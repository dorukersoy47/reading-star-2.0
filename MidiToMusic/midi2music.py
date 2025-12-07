import fluidsynth
import pretty_midi
import json
import soundfile
import sounddevice
import numpy
import struct
import os

audioBankPath = "/Users/sinansensurucu/VSCode/UCL Code/Second Year/COMP0016/reading-star-2.0/MidiToMusic/Audio_Bank/ReadingStar 2.0.sf2"
midiBankPath  = "/Users/sinansensurucu/VSCode/UCL Code/Second Year/COMP0016/reading-star-2.0/MidiToMusic/MIDI_Bank/TestMIDI.json"

sampleRate    = 44100
tailInSeconds = 1.0

def getSf2Preset(sf2Path, instrument, channel):
    fs = fluidsynth.Synth()
    soundfileID = fs.sfload(sf2Path)
    fs.delete()

    inst_lower = instrument.lower()

    with open(sf2Path, "rb") as f:
        if f.read(4) != b"RIFF":
            raise ValueError("Not a RIFF file")
        _ = f.read(4)
        if f.read(4) != b"sfbk":
            raise ValueError("Not a SoundFont2 (sfbk) file")

        pdta_offset = None
        pdta_size = None

        while True:
            header = f.read(8)
            if len(header) < 8:
                break

            chunk_id, chunk_size = struct.unpack("<4sI", header)

            if chunk_id == b"LIST":
                list_type = f.read(4)
                if list_type == b"pdta":
                    pdta_offset = f.tell()
                    pdta_size = chunk_size - 4
                    break
                else:
                    f.seek(chunk_size - 4, 1)
            else:
                f.seek(chunk_size, 1)

        if pdta_offset is None:
            raise ValueError("pdta chunk not found")

        f.seek(pdta_offset)
        end_pdta = pdta_offset + pdta_size
        phdr_data = None

        while f.tell() < end_pdta:
            sub_header = f.read(8)
            if len(sub_header) < 8:
                break

            sub_id, sub_size = struct.unpack("<4sI", sub_header)

            if sub_id == b"phdr":
                phdr_data = f.read(sub_size)
                break
            else:
                f.seek(sub_size, 1)

        if phdr_data is None:
            raise ValueError("phdr chunk not found")

        record_size = 38
        count = len(phdr_data) // record_size

        for i in range(count - 1):
            base = i * record_size
            rec = phdr_data[base:base + record_size]

            raw_name = rec[0:20]
            name = raw_name.split(b"\x00", 1)[0].decode("ascii", errors="ignore")
            preset_num, bank_num = struct.unpack_from("<HH", rec, 20)

            if name.lower() == inst_lower:
                return (channel, soundfileID, bank_num, preset_num)

    raise ValueError(f"Preset '{instrument}' not found in {sf2Path}")


def loadMIDIData(midiFilePath):
    with open(midiFilePath, "r") as midiFile:
        midiData = json.load(midiFile)
        return midiData


def processMIDIData(midiData, loopBars=None):
    bpm            = midiData["tempo"]
    secondsPerBeat = 60.0 / bpm
    beatsPerBar    = int(midiData["time_signature"].split("/")[0])

    midiEvents = []

    for track in midiData["tracks"]:
        channel = track["channel"]

        for note in track["notes"]:
            bar      = note["bar"]
            beat     = note["beat"]
            pitch    = note["pitch"]
            velocity = note["velocity"]

            startTime = ((bar - 1) * beatsPerBar + (beat - 1)) * secondsPerBeat

            midiEvents.append((startTime, "on",  channel, pitch, velocity))
            #midiEvents.append((endTime,   "off", channel, pitch, 0))

    midiEvents.sort(key=lambda e: e[0])

    if loopBars is None:
        return midiEvents

    baseLengthBars = midiData.get("length_bars")
    if not baseLengthBars:
        maxBar = 1
        for track in midiData["tracks"]:
            for note in track["notes"]:
                if note["bar"] > maxBar:
                    maxBar = note["bar"]
        baseLengthBars = maxBar

    secondsPerBar    = beatsPerBar * secondsPerBeat
    patternDuration  = baseLengthBars * secondsPerBar

    loops = max(1, int(loopBars / baseLengthBars))

    loopedEvents = []
    for i in range(loops):
        offset = i * patternDuration
        for (t, activation, channel, pitch, velocity) in midiEvents:
            loopedEvents.append((t + offset, activation, channel, pitch, velocity))

    loopedEvents.sort(key=lambda e: e[0])
    return loopedEvents


def renderMIDIData(midiEvents, midiData, channelVolumes, overallVolume):
    fluidsynthInstance = fluidsynth.Synth(samplerate=sampleRate)
    soundfileID = fluidsynthInstance.sfload(audioBankPath)

    channelsInUse = sorted({event[2] for event in midiEvents})

    channelToName = {track["channel"]: track["name"] for track in midiData["tracks"]}

    for channel in channelsInUse:
        instrumentName = channelToName.get(channel)
        if instrumentName is None:
            raise ValueError(f"No instrument name found in JSON for channel {channel}")

        _, _, bank, program = getSf2Preset(audioBankPath, instrumentName, channel)
        fluidsynthInstance.program_select(channel, soundfileID, bank, program)

    for channel in channelsInUse:
        vol = channelVolumes.get(channel, 100)
        fluidsynthInstance.cc(channel, 7, vol)

    totalTime   = midiEvents[-1][0] + tailInSeconds
    totalFrames = int(totalTime * sampleRate)

    audio = numpy.zeros(totalFrames * 2, dtype=numpy.int16)

    currentMIDIEventIndex = 0
    midiEventCount        = len(midiEvents)

    blockSize     = 512
    framePosition = 0
    currentTime   = 0.0

    while framePosition < totalFrames:
        while currentMIDIEventIndex < midiEventCount and midiEvents[currentMIDIEventIndex][0] <= currentTime:
            _, activation, channel, pitch, velocity = midiEvents[currentMIDIEventIndex]

            if activation == "on":
                fluidsynthInstance.noteon(channel, pitch, velocity)
            else:
                fluidsynthInstance.noteoff(channel, pitch)

            currentMIDIEventIndex += 1

        framesLeft = totalFrames - framePosition
        thisBlock  = min(blockSize, framesLeft)

        samples = fluidsynthInstance.get_samples(thisBlock)
        audio[framePosition * 2 : framePosition * 2 + thisBlock * 2] = samples

        framePosition += thisBlock
        currentTime   += thisBlock / sampleRate

    if overallVolume != 1.0:
        tmp = audio.astype(numpy.int32)
        tmp = (tmp * overallVolume).clip(-32768, 32767)
        audio = tmp.astype(numpy.int16)

    audio = audio.reshape(-1, 2)
    soundfile.write("llm_render.wav", audio, sampleRate)

    fluidsynthInstance.delete()

def interactiveRender(midiEvents, midiData):
    channelsInUse = sorted({event[2] for event in midiEvents})

    channelToName = {track["channel"]: track["name"] for track in midiData["tracks"]}

    channelVolumes = {
        channel: 80
        for channel in channelsInUse
    }

    overallVolume = 1.0

    while True:
        print("\nCurrent mix settings:")
        print(f"- Song volume: {overallVolume:.2f}")
        for channel in channelsInUse:
            name = channelToName.get(channel, f"Channel {channel}")
            print(f"- {name} volume: {channelVolumes[channel]}")
        print()

        renderMIDIData(midiEvents, midiData, channelVolumes, overallVolume)


        print("Options:")
        print("1) Accept mix and exit.")
        print("2) Change individual instrument volumes.")
        print("3) Change overall song volume.")
        choice = input("Enter choice number [1,2,3]: ").strip()

        if choice == "1":
            print("Mix accepted. Exiting.")
            break

        elif choice == "3":
            gain_str = input(f"Enter new song volume (currently at {overallVolume:.2f}) [0-5.0]: ").strip()
            try:
                newOverallVolume = float(gain_str)
                if newOverallVolume <= 0 or newOverallVolume > 5.0:
                    raise ValueError()
                overallVolume = newOverallVolume
                print(f"Song volume set to {overallVolume:.2f}. Re-rendering...")
                print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
            except ValueError:
                print("Invalid volume value, keeping old volume.")
            continue

        elif choice == "2":
            print("\nInstruments:")
            indexed_instruments = []
            for idx, channel in enumerate(channelsInUse):
                instrumentName = channelToName.get(channel, f"Channel {channel}")
                indexed_instruments.append((idx, channel, instrumentName))
                print(f"  [{idx}] {instrumentName} (current volume: {channelVolumes[channel]})")

            idx_str = input("Enter the number of the instrument you want to change (or press Enter to cancel): ").strip()
            if idx_str == "":
                continue

            try:
                idx = int(idx_str)
                _, channel, instrumentName = indexed_instruments[idx]
            except (ValueError, IndexError):
                print("Invalid selection, try again.")
                continue

            volumeString = input(f"Enter new volume for '{instrumentName}' (0–127): ").strip()
            try:
                vol = int(volumeString)
                if not 0 <= vol <= 127:
                    raise ValueError()
            except ValueError:
                print("Invalid volume, keeping old value.")
                continue

            channelVolumes[channel] = vol
            print(f"Updated '{instrumentName}' volume to {vol}. Re-rendering...\n")
            continue

        else:
            print("Unknown option, please choose 1, 2, or 3.")
            continue

def main():
    midiData = loadMIDIData(midiBankPath)

    bpm            = midiData["tempo"]
    secondsPerBeat = 60.0 / bpm
    beatsPerBar    = int(midiData["time_signature"].split("/")[0])
    secondsPerBar  = beatsPerBar * secondsPerBeat

    baseLengthBars = midiData.get("length_bars", 4)

    optionsBars = [baseLengthBars * 2, baseLengthBars * 4, baseLengthBars * 8]

    for i, bars in enumerate(optionsBars, start=1):
        secs = bars * secondsPerBar
        print(f"{i}) Loop for {bars} bars ({secs:.1f} seconds)")

    choice = input("Enter choice number (defaults to 8 bars): ").strip()
    try:
        choiceIdx = int(choice) if choice else 1
    except ValueError:
        choiceIdx = 1

    choiceIdx = max(1, min(choiceIdx, len(optionsBars)))
    loopBars  = optionsBars[choiceIdx - 1]

    midiEvents = processMIDIData(midiData, loopBars=loopBars)
    interactiveRender(midiEvents, midiData)

    


if __name__ == "__main__":
    main()
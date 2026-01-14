from pathlib import Path
from generator import generate_music


def main():
    # Define where you want files to go
    save_dir = Path("./generated_music")

    choice = 0
    while choice != "11":
        print("\n" + "=" * 50)
        print(f"Saving to: {save_dir.absolute()}")
        choice = input("Choose a genre (~2 minute extended versions):\n"
                       "1. Nursery Rhyme\n"
                       "2. Hip-Hop\n"
                       "3. Rock\n"
                       "4. Jazz\n"
                       "5. Classical\n"
                       "6. Reggae\n"
                       "7. R&B\n"
                       "8. Punk\n"
                       "9. Metal\n"
                       "10. Bollywood\n"
                       "11. Quit\n"
                       "Enter number: ")

        genre_map = {
            "1": "nursery_rhyme",
            "2": "hip_hop",
            "3": "rock",
            "4": "jazz",
            "5": "classical",
            "6": "reggae",
            "7": "rnb",
            "8": "punk",
            "9": "metal",
            "10": "bollywood"
        }

        if choice in genre_map:
            generate_music(genre_map[choice], output_folder=save_dir)
        elif choice == "11":
            print("\nGoodbye!")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
from googlesearch import search


def fetch_google_results(query):
    try:
        return list(search(query, num_results=3))
    except Exception as e:
        print("An error occurred:", e)
        return []


def main():
    query = input("Enter your search query: ")

    results = fetch_google_results(query)

    if results:
        print("\nTop", "results for:", query)
        for idx, result in enumerate(results):
            print(idx, "-", result)
    else:
        print("No results found.")


if __name__ == "__main__":
    main()

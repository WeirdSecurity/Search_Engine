from Inverted_Indexing import NLTKInvertedIndex

def main():
    # Initialize the indexer
    index = NLTKInvertedIndex()
    
    # Load the data from index.json
    print("Loading search index...")
    index.load_index()
    
    if not index.index:
        print("Warning: The index is empty. Please run Web_Scraper.py first to crawl some pages.")
    else:
        print(f"Index loaded successfully with {len(index.index)} terms.")

    print("\n" + "="*40)
    print("  WELCOME TO MINI-SEARCH (Ranked)")
    print("="*40)
    print("Type 'exit' or 'quit' to stop searching.\n")

    while True:
        query = input("Search query: ").strip()
        
        if query.lower() in ['exit', 'quit']:
            break
            
        if not query:
            continue

        results = index.search(query)
        
        if not results:
            print(f"No results found for '{query}'.")
        else:
            print(f"\nFound {len(results)} matching URLs:")
            # results is now a list of tuples: [(url, score), (url, score)]
            for i, (link, score) in enumerate(results[:10], 1):
                meta = index.metadata.get(link, {})
                title = meta.get('title', 'No Title')
                snippet = meta.get('snippet', 'No description available.')
                
                print(f"{i}. {title}")
                print(f"   [Score: {score}] {link}")
                print(f"   {snippet}\n")
        print("-" * 40)

if __name__ == "__main__":
    main()

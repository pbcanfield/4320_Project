from Manager import DataManager

if __name__ == '__main__':
    manager = DataManager()

    print("Repository Names: ", end='')
    print(manager.list_repos(), end='\n\n')
    
    print("Contributor Names: ", end='')
    print(manager.list_names('augur'), end='\n\n')

    print("Contributor Names: ", end='')
    print(manager.list_names('grimoirelab'), end='\n\n')

    #manager.display_df()

    print("Visualization Functions")
    manager.display_most_contributions()

    print("Search Functions") 
    manager.get_pie_by_name('GeorgLink')
    manager.search_similar_contributions('augur','open_pull_request')


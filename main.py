from Manager import DataManager
from ContribUI import ContribUI

if __name__ == '__main__':

    '''
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
    '''
    manager = DataManager()

    manager.display_df()

    #print(manager.get_action_types())

    contribui = ContribUI(className='UI')
    contribui.initialize(data_manager=manager)
    contribui.mainloop()


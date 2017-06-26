from selenium import webdriver
import getpass
import time
import os

def approve_and_merge(repo_url, base_fork_username=None):
    '''
    Input (String): repo_url is the full website URL of the repository to update.
                    base_fork_username (optional) specifies the base fork repository
                    to compare when creating pull request.
                    base_fork_username is default to origin repository.
    
    This method navigates to repo_url and attempts to sign-in with given user
    and pw. This method will then navigate to the OEC repo's "systems" directory and
    upload (overwrite if same file name exists) the old XML files with the
    updated XML files in "all_xml" local directory and commit the changes.
    Then, an attempt will be made to create a pull request for the changes
    and merge to origin repository or base_fork_username forked repository if specified.
    
    Pull request will fail if there are pending pull requests for the changes
    or if base_fork_username does not exist.
    
    Merge will fail if the signed-in user does not have sufficient privileges to
    perform the merge, but the pull request will remain in the target repository.
    '''
    cwd = os.getcwd()
    oec_systems = os.path.join(cwd, "systems")
    all_xml_path = os.path.join(cwd, "all_xml")
    repo_name = repo_url.split('/')[-1]
    page_load_buffer = 1 # seconds
    
    try:
        driver = webdriver.Chrome()
        
        # comment this out if you want to see the actions performed in browser
        driver.set_window_position(9001,9001)
        
        # Navigate to GitHub and sign in
        driver.get(repo_url)
        time.sleep(page_load_buffer)
        
        # find sign-in button
        try:
            element = driver.find_element_by_xpath("//*[@id=\"login\"]/form/div[4]/input[3]")
        except:
            element = driver.find_element_by_xpath("/html/body/header/div/div/div/a[2]")
        
        # attempt to login
        try:
            time.sleep(page_load_buffer)
            element.click()
            print("Sign into GitHub")
            user = input("Enter your username or email address: ")
            pw = getpass.getpass("Enter your password: ")
            element = driver.find_element_by_xpath("//*[@id=\"login_field\"]")
            time.sleep(page_load_buffer)
            element.send_keys(user)
            element = driver.find_element_by_xpath("//*[@id=\"password\"]")
            time.sleep(page_load_buffer)
            element.send_keys(pw)
            element = driver.find_element_by_xpath("//*[@id=\"login\"]/form/div[4]/input[3]")
            time.sleep(page_load_buffer)
            element.click()
            print("Attempting to sign in...")            
        except:
            pass # already logged in
            
        # if fail to login, keep asking to login until successful
        while "Sign in" in driver.title:
            element = driver.find_element_by_xpath("//*[@id=\"login_field\"]")
            time.sleep(page_load_buffer)
            element.clear()
            element = driver.find_element_by_xpath("//*[@id=\"password\"]")
            time.sleep(page_load_buffer)
            element.clear()
            print("Incorrect username or password. Please try again.")
            user = input("Enter your username or email address: ")
            pw = getpass.getpass("Enter your password: ")
            element = driver.find_element_by_xpath("//*[@id=\"login_field\"]")
            time.sleep(page_load_buffer)
            element.send_keys(user)
            element = driver.find_element_by_xpath("//*[@id=\"password\"]")
            time.sleep(page_load_buffer)
            element.send_keys(pw)
            element = driver.find_element_by_xpath("//*[@id=\"login\"]/form/div[4]/input[3]")
            time.sleep(page_load_buffer)
            element.click()
            print("Attempting to sign in...")
            
        # login successful
        time.sleep(page_load_buffer)
        print("Sign in successful!")
        time.sleep(page_load_buffer)
        
        # click "fork" button
        element = driver.find_element_by_xpath("//*[@id=\"js-repo-pjax-container\"]/div[1]/div[1]/ul/li[3]/a[1]")
        element.click()
        
        # create user fork repo if it doesn't exist
        try:
            time.sleep(page_load_buffer)
            element = driver.find_element_by_xpath("//*[@id=\"facebox\"]/div/div/form/div[2]/button/img")
            print("Forking repository...")
            element.click()
            while ":" not in driver.title:
                time.sleep(page_load_buffer)
            print("Repository successfully forked!")
        # user fork repo already exists, go to forked repo
        except:
            time.sleep(page_load_buffer)
            element = driver.find_element_by_xpath("//*[@id=\"facebox\"]/div/div/form/ul[1]")
            element = driver.find_element_by_partial_link_text(user + '/' + repo_name)
            element.click()
            time.sleep(page_load_buffer)
            
        # build URL to navigate to systems folder on oec_auto_update branch
        start_offset = oec_systems.find(repo_name)
        end_offset = oec_systems[start_offset:].find('\\') + 1
        dir_list = oec_systems[start_offset+end_offset:].split('\\')
        url = driver.current_url
        
        if '/tree/master' not in url:
            url += '/tree/master'
            
        for d in dir_list:
            url = url + '/' + d
            
        # Navigate to systems folder and upload the updated xml_file (overwrites old file)
        print("Navigating to " + url + "...")
        driver.get(url)
        time.sleep(page_load_buffer)
        print("Uploading updated XML file...")
        element = driver.find_element_by_xpath("//*[@id=\"js-repo-pjax-container\"]/div[2]/div[1]/div[1]/div[2]/a[1]")
        element.click()
        time.sleep(page_load_buffer)
        element = driver.find_element_by_xpath("//*[@id=\"js-repo-pjax-container\"]/div[2]/div[1]/div[2]/form[2]/div[2]/p/input")
        time.sleep(page_load_buffer)
        for xml_file in os.listdir(all_xml_path):
            element.send_keys(os.path.join(all_xml_path, xml_file))
        driver.implicitly_wait(30)
        print("Upload successful!")
        
        # Enter commit summary and description
        print("Preparing to commit uploaded file...")
        element = driver.find_element_by_xpath("//*[@id=\"commit-summary-input\"]")
        time.sleep(page_load_buffer)
        element.send_keys("OEC Auto Update")
        element = driver.find_element_by_xpath("//*[@id=\"commit-description-textarea\"]")
        time.sleep(page_load_buffer)
        element.send_keys("OEC Auto Update")
        
        # Commit the updated XML file
        print("Committing uploaded file...")
        element = driver.find_element_by_xpath("//*[@id=\"js-repo-pjax-container\"]/div[2]/div[1]/form/button")
        time.sleep(page_load_buffer)
        element.click()
        driver.implicitly_wait(30)
        print("Commit successful!")
        
        # Create new pull request
        print("Creating new pull request...")
        time.sleep(page_load_buffer)
        
        try:
            element = driver.find_element_by_xpath("//*[@id=\"js-repo-pjax-container\"]/div[2]/div[1]/div[4]/a")
            element.click()
        except:
            element = driver.find_element_by_xpath("//*[@id=\"js-repo-pjax-container\"]/div[2]/div[1]/div[5]/a")
            element.click()
            
        time.sleep(page_load_buffer)
        
        # pull request to base_fork_username/repo_name if specified instead of origin
        if base_fork_username != None:
            try:
                element = driver.find_element_by_xpath("//*[@id=\"js-repo-pjax-container\"]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/button/span")
                element.click()
                time.sleep(page_load_buffer)
                element = driver.find_element_by_xpath("//*[@id=\"pull-repo-filter-field-base\"]")
                element.send_keys(base_fork_username + '/' + repo_name)
                time.sleep(page_load_buffer)
                element = driver.find_element_by_xpath("//*[@id=\"js-repo-pjax-container\"]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div/div/div[3]/div[1]")
                element.click()
                time.sleep(page_load_buffer)
            except:
                print("Specified base fork repository does not exist.")
                driver.quit()
                return
        
        # try to find create pull request button
        # if there are existing pull requests (conflict), the button will not show
        try:
            element = driver.find_element_by_xpath("//*[@id=\"js-repo-pjax-container\"]/div[2]/div[1]/div[2]/div/button")
            element.click()
        except:
            print("There are pending pull requests to the target repository.")
            print("Please resolve the conflicts before continuing.")
            driver.quit()
            return
        
        time.sleep(page_load_buffer)
        
        # in case of multiple commits, check for pull request details
        # if details are blank, enter generic auto update details
        pull_title = driver.find_element_by_xpath("//*[@id=\"pull_request_title\"]")
        pull_comment = driver.find_element_by_xpath("//*[@id=\"pull_request_body\"]")
        if pull_title.get_attribute("value") == '':
            pull_title.send_keys("OEC Auto Update")
        if pull_comment.get_attribute("value") == '':
            pull_comment.send_keys("OEC Auto Update")
            
        element = driver.find_element_by_xpath("//*[@id=\"new_pull_request\"]/div[2]/div/div/div[3]/button")
        element.click()
        time.sleep(page_load_buffer)
        print("Pull request successfully created!")
        
        # Merge pull request
        print("Attempting to merge pull request...")
        try:
            element = driver.find_element_by_xpath("//*[@id=\"partial-pull-merging\"]/div[1]/div/div/div/div[2]/div[1]/div[1]/button[1]")
            element.click()
            time.sleep(page_load_buffer)
            element = driver.find_element_by_xpath("//*[@id=\"merge_title_field\"]")
            element.send_keys(" (OEC Auto Update)")
            time.sleep(page_load_buffer)
            element = driver.find_element_by_xpath("//*[@id=\"partial-pull-merging\"]/div[1]/form/div[2]/div[2]/div/div[1]/button")
            element.click()
            print("Merge successful!")
            driver.quit()
        except:
            print("You do not have permissions to merge.")
            print("Please contact owner to merge the pull request.")
            driver.quit()
        
    except:
        print("Either page failed to load or user has insufficient permissions")
        print("Please check the following:")
        print("1. Internet connection")
        print("2. GitHub account permissions")
        print("3. Method is being run from a valid clone repository")
        print("4. Increase page_load_buffer time in method")
        driver.quit()    
                
# Example Usage (safe tests)
#approve_and_merge("https://github.com/CSCC01-Fall2016/team14-Project")
#approve_and_merge("https://github.com/CSCC01-Fall2016/team14-Project", "CSCC01-Fall2016")
#approve_and_merge("https://github.com/CSCC01-Fall2016/team14-Project", "adwen")
#approve_and_merge("https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue", "adwen")
#approve_and_merge("https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue", "btang02")

'''
WARNING!!!
Below example is for absolute final release (pull request to the MAIN OEC REPO)
EXAMPLE IS ONLY TO SHOW METHOD USAGE, DO NOT ACTUALLY USE IN DEMO OR TESTING
'''
# approve_and_merge("https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue")
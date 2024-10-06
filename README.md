# crowdfunding_back_end
Culture4Kids: Empowering Aboriginal and Torres Strait Islander kids

## Planning:
### Concept/Name
The crowdfunding platform Culture4Kids connects Aboriginal and Torres Strait Islander kids who have been taken into State care with their culture, country and community through supporting grassroots cultural programs like dance, art, traditional practices, language classes, cultural camps, on country trips, boys cultural pathways, or girls cultural pathways. Aboriginal led organisations who are looking to crowdfund existing cultural programs or would like to add new cultural programs, can add/create the cultural program as a campaign/project to raise funds. 

### Intended Audience/User Stories
Who are your intended audience? 
- Aboriginal and/or Torres Strait Islander Community Controlled Organisations (ACCOs)
- Aboriginal and/or Torres Strait Islander Corporations
- Aboriginal and/or Torres Strait Islander Community Centres
- Aboriginal and/or Torres Strait Islander language centres

How will they use the website?
User stories
=> Log in
    - Log in
    - Sign up
=> Homepage
    - See list of available crowdfunding projects
=> "My Profile"
    - See details of currently-logged-in user account
    - change details of user account
    - delete user account (?)
=> "My Campaigns"

### Front End Pages/Functionality
- {{ A page on the front end }}
    - {{ A list of dot-points showing functionality is available on this page }}
    - {{ etc }}
    - {{ etc }}
- {{ A second page available on the front end }}
    - {{ Another list of dot-points showing functionality }}
    - {{ etc }}

### API Spec
{{ Fill out the table below to define your endpoints. An example of what this might look like is shown at the bottom of the page. 

It might look messy here in the PDF, but once it's rendered it looks very neat! 

It can be helpful to keep the markdown preview open in VS Code so that you can see what you're typing more easily. }}

| URL | HTTP Method | Purpose | Request Body | Success Response Code | Authentication/Authorisation |
| :------ | :----------- | :------- | :------- | :------------ | :--------------------- | :---------------------------- |
| /projects/ | GET | Returns all projects. | N/A | 200 | N/A |
| /projects/ | POST | Create new project. | Project object | 201 | Must be logged in. |

### DB Schema
![]( {{ ./relative/path/to/your/schema/image.png }} )
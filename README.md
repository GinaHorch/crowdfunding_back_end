## Project Description
Kickstarter, Go Fund Me, Kiva, Change.org, Patreon… All of these different websites have something in common: they provide a platform for people to fund projects that they believe in, but they all have a slightly different approach. You are going to create your own crowdfunding website, and put your own spin on it!

## Project Requirements
Your crowdfunding project must:

- [ ] Be separated into two distinct projects: an API built using the Django Rest Framework and a website built using React. 
- [x] Have a cool name, bonus points if it includes a pun and/or missing vowels. See https://namelix.com/ for inspiration. <sup><sup>(Bonus Points are meaningless)</sup></sup>
- [x] Have a clear target audience.
- [x] Have user accounts. A user should have at least the following attributes:
  - [x] Username
  - [x] Email address
  - [x] Password
- [x] Ability to create a “project” to be crowdfunded which will include at least the following attributes:
  - [x] Title
  - [x] Owner (a user)
  - [x] Description
  - [x] Image
  - [x] Target amount to fundraise
  - [x] Whether it is currently open to accepting new supporters or not
  - [x] When the project was created
- [x] Ability to “pledge” to a project. A pledge should include at least the following attributes:
  - [x] An amount
  - [x] The project the pledge is for
  - [x] The supporter/user (i.e. who created the pledge)
  - [x] Whether the pledge is anonymous or not
  - [x] A comment to go along with the pledge
- [ ] Implement suitable update/delete functionality, e.g. should a project owner be allowed to update a project description?
- [ ] Implement suitable permissions, e.g. who is allowed to delete a pledge?
- [ ] Return the relevant status codes for both successful and unsuccessful requests to the API.
- [ ] Handle failed requests gracefully (e.g. you should have a custom 404 page rather than the default error page).
- [ ] Use Token Authentication, including an endpoint to obtain a token along with the current user's details.
- [ ] Implement responsive design.

## Additional Notes
No additional libraries or frameworks, other than what we use in class, are allowed unless approved by the Lead Mentor.

Note that while this is a crowdfunding website, actual money transactions are out of scope for this project.

## Submission
To submit, fill out [this Google form](https://forms.gle/34ymxgPhdT8YXDgF6), including a link to your Github repo. Your lead mentor will respond with any feedback they can offer, and you can approach the mentoring team if you would like help to make improvements based on this feedback!

Please include the following in your readme doc:
- [ ] A link to the deployed project.
- [ ] A screenshot of Insomnia, demonstrating a successful GET method for any endpoint.
- [ ] A screenshot of Insomnia, demonstrating a successful POST method for any endpoint.
- [ ] A screenshot of Insomnia, demonstrating a token being returned.
- [ ] Step by step instructions for how to register a new user and create a new project (i.e. endpoints and body data).
- [ ] Your refined API specification and Database Schema.

# crowdfunding_back_end
Culture4Kids: Empowering Aboriginal and Torres Strait Islander kids

## Planning:
### Concept/Name
The crowdfunding platform Culture4Kids connects Aboriginal and Torres Strait Islander kids who have been taken into State care with their culture, country and community through supporting grassroots cultural programs like dance, art, traditional practices, language classes, cultural camps, on country trips, boys cultural pathways, or girls cultural pathways. Aboriginal led organisations who are looking to crowdfund existing cultural programs or would like to add new cultural programs, can add/create the cultural program as a project to raise funds. There will be an indication if the organisation is a registered charity with the option to receive tax invoices for donations of more than $2AUD.

### Intended Audience/User Stories
Who are your intended audience (creating projects)? 
- Aboriginal and/or Torres Strait Islander Community Controlled Organisations (ACCOs)
- Aboriginal and/or Torres Strait Islander Corporations
- Aboriginal and/or Torres Strait Islander Community Centres
- Aboriginal and/or Torres Strait Islander language centres

Who are your intended audience (supporters/pledges)
- Anyone with spare money
  
How will they use the website?
User stories
=> Log in as user/supporter
    - Sign up
    - Log in
    - View categories with projects
    - View projects by organisation
    - Browse projects
    - Make pledges to projects
  
=> Log in as user/organisation
    - Sign up/create organisation/owner
    - Admin status for owner of organisation
    - Approve additional users/members of the organisation
    - Changes to organisation details only by organisation/owner
    - Create projects by organisation/owner and organisation/member
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
| --- | --- | --- | --- | --- | --- |
| /projects/ | GET | Returns all projects. | N/A | 200 | N/A |
| /projects/ | POST | Create new project. | Project object | 201 | Must be logged in. |
| /users/ | GET | Returns all users. | not sure | 200 | Must be superuser. |

### DB Schema
![]( {{ ./relative/path/to/your/schema/image.png }} )
| URL | HTTP Method | Purpose | Request Body | Success Response Code | Authentication/Authorisation |
| --- | --- | --- | --- | --- | --- |
| /projects/ | GET | Returns all projects. | N/A | 200 | N/A |
| /projects/ | POST | Create new project. | Project object | 201 | Must be logged in. |

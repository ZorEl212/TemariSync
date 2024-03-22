# TemariSync
TemariSync is a web application designed to manage, organize and share academic resources among students. It provides a user-friendly interface for users to interact with their data. <br>
Link to deployed site [Here](https://yabsirad212.wixsite.com/temarisync-2)<br>
Link to [Blog](https://www.linkedin.com/pulse/introducing-temarisync-streamlining-academic-yeabsira-desalegn-xis6c/) about TemariSync <br>
Author Yeabsira Desalegn: [LinkedIn](https://www.linkedin.com/in/yeabsira-desalegn-8a706a297/)

## Features

- User authentication: Users can log in to access their data. Unauthorized access is prevented.
- Assignments, Projects, and Materials: Users can store their resources remotely in an organized manner.
- Seamless access to your materials, you can retrieve documents instantly, whether you're at home, in the library, or on the go.
- Share resources with peers, students can share their documents with their peers with ease

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- A modern web browser
- A server to host the application
- A webserver configured to reverse proxy to the app
- The MySQL database root user should be properly configured.



# Installation

## Setting up environment
 - Clone the repository to your local machine or server and navigate to the cloned repository.
 - Install required packages by running `setup-env.sh` with root privileges.
 - Unless you want to use custom database configurations, set up the default database by running `cat database.sql | mysql -u root -p`

## Running the app

1. If you are going to use custom database configurations, edit `run-api.sh` to modify database configurations. Otherwise, proceed to the next step.
2. Generate a secret key to be used to encrypt session cache. It is recommended to use a strong random string.
3. Start the API with `SECRET_KEY='Your Secret Key' ./run-api.sh`
4. Finally, start the front-end by running `run-app.sh`
5. Now the app should be ready to go. Navigate to the domain you configured and access it.


## Usage

1. Log in with your user credentials or create a new User.
2. Use the navigation links to access the site accordingly.
3. Click the logout button to log out of your account.

## API Endpoints

The application uses the following API endpoints:

Check all API endpoints [here](API-DOCUMENTATION.md)

## Contributing

We welcome contributions from the community to help improve TemariSync. If you have any ideas, bug reports, or feature requests, please feel free to contact us or submit a pull request. We appreciate your support in making TemariSync even better!

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
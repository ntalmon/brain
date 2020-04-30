import React from "react";
import ReactDOM from "react-dom";
import "./index.css";

var API_ROOT = "http://127.0.0.1:5000";

class User extends React.Component {
  render() {
    return <div>{this.props.userName}</div>;
  }
}

class App extends React.Component {
  constructor() {
    super();
    this.state = { users: [] };
  }
  render() {
    var usersList = [];
    this.state.users.forEach((user) => {
      usersList.push(
        <li>
          <User userId={user.userj_id} userName={user.username} />
        </li>
      );
    });
    return (
      <div className="App">
        <ul>{usersList}</ul>
      </div>
    );
  }
  componentDidMount() {
    fetch(API_ROOT + "/users").then(
      function (response) {
        response.json().then(
          function (data) {
            this.setState({ users: data });
          }.bind(this)
        );
      }.bind(this)
    );
  }
}

ReactDOM.render(<App />, document.getElementById("root"));

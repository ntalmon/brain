import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom";
import "./index.css";
import "./users-list.css";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

var API_ROOT = "http://127.0.0.1:5000";

class Result extends React.Component {
  constructor(props) {
    super(props);
    this.state = { resultValue: null };
  }
  render() {
    switch (this.props.result) {
      case "pose":
        return <div>{JSON.stringify(this.state.resultValue)}</div>;
      case "color-image":
      case "depth-image":
        return (
          <img
            src={this.props.url + "/" + this.props.result + "/data"}
            width="500"
            height="500"
          />
        );
      case "feelings":
        return <div>{JSON.stringify(this.state.resultValue)}</div>;
    }
    return <div></div>;
  }
  componentDidMount() {
    fetch(this.props.url + "/" + this.props.result).then(
      function (response) {
        response.json().then(
          function (data) {
            this.setState({ resultValue: data });
          }.bind(this)
        );
      }.bind(this)
    );
  }
}

class Post extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      userId: props.userId,
      snapshotId: props.snapshotId,
      datetime: props.datetime,
      results: [],
    };
  }
  render() {
    let results = [];
    this.state.results.forEach(
      function (result) {
        let url =
          API_ROOT +
          "/users/" +
          this.props.userId +
          "/snapshots/" +
          this.props.snapshotId;
        let collapse = <Result url={url} result={result} />;
        results.push(collapse);
      }.bind(this)
    );
    let date = new Date(1000 * this.props.datetime);
    return (
      <div>
        <h1>#{this.props.snapshotId}</h1>
        <h2>{this.props.datetime}</h2>
        {results}
      </div>
    );
  }

  componentDidMount() {
    fetch(
      API_ROOT +
        "/users/" +
        this.state.userId +
        "/snapshots/" +
        this.state.snapshotId
    ).then(
      function (response) {
        response.json().then(
          function (data) {
            this.setState({ results: data.results });
          }.bind(this)
        );
      }.bind(this)
    );
  }
}

class Posts extends React.Component {
  constructor(props) {
    super(props);
    this.state = { userId: props.userId, snapshots: [] };
  }
  render() {
    var posts = [];
    this.state.snapshots.forEach(
      function (snapshot) {
        posts.push(
          <div className="post">
            <Post
              userId={this.props.userId}
              snapshotId={snapshot.uuid}
              datetime={snapshot.datetime}
            />
          </div>
        );
      }.bind(this)
    );
    return <div>{posts}</div>;
  }
  componentDidMount() {
    fetch(API_ROOT + "/users/" + this.state.userId + "/snapshots").then(
      function (response) {
        response.json().then(
          function (data) {
            this.setState({ snapshots: data });
          }.bind(this)
        );
      }.bind(this)
    );
  }
}

class User extends React.Component {
  constructor(props) {
    super(props);
    this.state = { initialis: "" };
  }

  render() {
    var userImage = <div className="userImage">{this.state.initials}</div>;
    return (
      <div>
        <div className="profile">
          {userImage}
          <h2 className="userNameText">{this.state.userName}</h2>
          <div>
            <span className="userDetail">User ID: {this.props.userId}</span>
            <span className="userDetail">Birthday: {this.state.birthday}</span>
            <span className="userDetail">Gender: {this.state.gender}</span>
          </div>
        </div>
        <div className="posts">
          <Posts userId={this.props.userId} />
        </div>
      </div>
    );
  }

  componentDidMount() {
    fetch(API_ROOT + "/users/" + this.props.userId).then(
      function (response) {
        response.json().then(
          function (data) {
            let firstLastName = data.username.split(" ");
            let initials = firstLastName[0][0] + firstLastName[1][0];
            this.setState({
              userName: data.username,
              birthday: data.birthday,
              gender: data.gender,
              initials: initials,
            });
          }.bind(this)
        );
      }.bind(this)
    );
  }
}

function UserPage({ match }) {
  let userId = match.params.id;
  return <User userId={userId} />;
}

class UserInList extends React.Component {
  render() {
    var firstLastName = this.props.userName.split(" ");
    var initials = firstLastName[0][0] + firstLastName[1][0];
    var userId = this.props.userId;
    return (
      <tr>
        <td>
          <div className="userImage">{initials}</div>
          <Link to={"/users/" + userId} class="user-link">
            {this.props.userName}
          </Link>
        </td>
        <td>
          <span>{this.props.userId}</span>
        </td>
      </tr>
    );
  }
}

class Users extends React.Component {
  constructor() {
    super();
    this.state = { users: [] };
  }
  render() {
    var users = [];
    this.state.users.forEach((user) => {
      users.push(<UserInList userId={user.user_id} userName={user.username} />);
    });
    return (
      <div className="OldApp">
        <div class="container bootstrap snippet">
          <div class="row">
            <div class="col-lg-12">
              <div class="main-box no-header clearfix">
                <div class="main-box-body clearfix">
                  <div class="table-responsive">
                    <table class="table user-list">
                      <thead>
                        <tr>
                          <th>
                            <span>User</span>
                          </th>
                          <th>
                            <span>User ID</span>
                          </th>
                        </tr>
                      </thead>
                      <tbody>{users}</tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
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

class Index extends React.Component {
  render() {
    return <Users key="Hi" />;
  }
}

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={Index} />
          <Route path="/users" exact component={Index} />
          <Route path="/users/:id" component={UserPage} />
        </Switch>
      </div>
    </Router>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));

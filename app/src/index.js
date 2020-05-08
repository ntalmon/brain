import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Users from "./users-page";

var isDebug = true;
var API_ROOT = isDebug ? "http://127.0.0.1:5000" : window.api_url;

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
        let feelings = this.state.resultValue;
        let hunger = feelings ? feelings.hunger : 0;
        return (
          <div>
            <label for="meter_hunger">
              <img src="/hunger.png" width="30" height="30" />
            </label>
            &nbsp; &nbsp;
            <meter id="meter_hunger" value={hunger} min="-1" max="1">
              0
            </meter>
          </div>
        );
      // return <div>{JSON.stringify(this.state.resultValue)}</div>;
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
      <div className="usersPage">
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

function Index() {
  return <Users />;
}

const Home = () => {
  return <span></span>;
};

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={Index} />
          <Route path="/users" exact component={Users} />
          <Route path="/users/:id" component={UserPage} />
        </Switch>
      </div>
    </Router>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));

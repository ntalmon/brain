import React from "react";
import ReactDOM from "react-dom";
import { Link } from "react-router-dom";
import "./index.css";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";
import Users from "./users-page";
import UserPage from "./user-page";

class Nav extends React.Component {
  constructor(props) {
    super(props);
    this.state = { redirect: false, path: "" };
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  render() {
    if (this.state.redirect) {
      // this.setState({ redirect: false });
      return <Redirect to={this.state.path} />;
    }
    return (
      <nav class="navbar navbar-expand-lg navbar-dark warning-color">
        <Link class="navbar-brand" to="/">
          Brain
        </Link>
        <div class="collapse navbar-collapse" id="basicExampleNav">
          <ul class="navbar-nav mr-left">
            <li class="nav-item">
              <Link class="nav-link" to="/users">
                Users
              </Link>
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                href="https://brain.readthedocs.io/en/latest/"
              >
                Documentation
              </a>
            </li>
          </ul>
        </div>
      </nav>
    );
  }
  handleSubmit(event) {
    event.preventDefault();
    this.setState({ redirect: true, path: "/users/" + event.target.value });
  }
}

function Index() {
  return <Users />;
}

function App() {
  return (
    <Router>
      <div className="App">
        <div className="main-nav">
          <Nav />
        </div>
        <div className="main-content">
          <Switch>
            <Route path="/" exact component={Index} />
            <Route path="/users" exact component={Users} />
            <Route path="/users/:id" component={UserPage} />
          </Switch>
        </div>
      </div>
    </Router>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));

import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Users from "./users-page";
import UserPage from "./user-page";

function Nav() {
  return (
    <nav class="navbar navbar-expand-lg navbar-dark primary-color">
      <a class="navbar-brand" href="#">
        Brain
      </a>
      &nbsp;
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#basicExampleNav"
        aria-controls="basicExampleNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="basicExampleNav">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#">
              Home
              <span class="sr-only">(current)</span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">
              Users
            </a>
          </li>
        </ul>
        <ul class="navbar-nav mr-left">
          <li class="nav-item">
            <form class="form-inline" id="user-navigation" for="#">
              <div class="md-form input-group my-0">
                <div class="input-group-prepend">
                  <span class="input-group-text" id="basic-addon11">
                    #
                  </span>
                </div>
                <input
                  type="text"
                  class="form-control"
                  placeholder="User ID"
                  aria-label="User ID"
                  aria-describedby="basic-addon11"
                />
              </div>
            </form>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="https://brain.readthedocs.io/en/latest/">
              Documentation
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
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

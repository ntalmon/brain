import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import "./index.css";
import Nav from "./components/nav";
import LandingPage from "./components/landing-page";
import UsersPage from "./components/users-page";
import UserPage from "./components/user-page";

function App() {
  return (
    <Router>
      <div className="App">
        <div className="main-nav">
          <Nav />
        </div>
        <div className="main-content">
          <Switch>
            <Route path="/" exact component={LandingPage} />
            <Route path="/users" exact component={UsersPage} />
            <Route path="/users/:id" component={UserPage} />
          </Switch>
        </div>
      </div>
    </Router>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));

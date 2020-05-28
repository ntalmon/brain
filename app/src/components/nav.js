import React from "react";
import PropTypes from "prop-types";
import { Link, withRouter } from "react-router-dom";
import "../css/nav.css";

class Nav extends React.Component {
  static propTypes = {
    match: PropTypes.object.isRequired,
    location: PropTypes.object.isRequired,
    history: PropTypes.object.isRequired,
  };

  constructor(props) {
    super(props);
    this.state = { active: "home" };
  }

  render() {
    let path = this.props.location.pathname;
    let homeClass = "nav-item" + (path === "/" ? " active" : "");
    let usersClass = "nav-item" + (path.startsWith("/users") ? " active" : "");

    return (
      <nav className="navbar navbar-expand-lg navbar-dark elegant-color">
        <Link className="navbar-brand" to="/">
          Brain
        </Link>

        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#basicExampleNav"
          aria-controls="basicExampleNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="basicExampleNav">
          <ul className="navbar-nav mr-auto">
            <li className={homeClass}>
              <Link className="nav-link" to="/">
                Home
              </Link>
            </li>
            <li className={usersClass}>
              <Link className="nav-link" to="/users">
                Users
              </Link>
            </li>
          </ul>

          <ul className="navbar-nav">
            <li className="nav-item" id="docs-link">
              <a
                className="nav-link"
                href="https://brain.readthedocs.io/en/latest/"
              >
                Docs
              </a>
            </li>
            <li className="nav-item">
              <a
                className="nav-link"
                id="github-link"
                href="https://github.com/noamtau1/brain"
              >
                <i className="fab fa-github fa-2x" id="github-link-icon"></i>
              </a>
            </li>
          </ul>
        </div>
      </nav>
    );
  }

  onClickHome = () => {
    this.setState({ active: "home" });
  };

  onClickUsers = () => {
    this.setState({ active: "users" });
  };
}

export default withRouter(Nav);

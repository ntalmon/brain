import React from "react";
import { Link } from "react-router-dom";
import "./users-page.css";


var isDebug = true;
var API_ROOT = isDebug ? "http://127.0.0.1:5000" : window.api_url;

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

export default Users;

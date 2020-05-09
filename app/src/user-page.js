import React, { useState, useEffect } from "react";
import { fetchAPI, formatURL, showTimestamp } from "./utils";
import "./user-page.css";

var defaultResults = {
  pose: {
    translation: { x: 0, y: 0, z: 0 },
    rotation: { x: 0, y: 0, z: 0, w: 0 },
  },
  "color-image": { path: "#" },
  "depth-image": { path: "#" },
  feelings: { hunger: 0, thirst: 0, exhaustion: 0, happiness: 0 },
};

const handlePose = (result) => {
  return (
    <ul>
      <li>
        Pose
        <br />
        Translation: (
        {[
          result.translation.x,
          result.translation.y,
          result.translation.z,
        ].join(", ")}
        )
        <br />
        Rotation: (
        {[
          result.rotation.x,
          result.rotation.y,
          result.rotation.z,
          result.rotation.w,
        ].join(", ")}
        )
      </li>
    </ul>
  );
};

const handleImage = (result) => {
  return <img src={result} width="500" height="500" />;
};

const handleFeelings = (result) => {
  return (
    <div>
      <br />
      <label htmlFor="meter_hunger">
        <img src="/hunger.png" width="30" height="30" />
      </label>
      &nbsp; &nbsp;
      <meter id="meter_hunger" value={result.hunger} min="-1" max="1"></meter>
      <br />
      <label htmlFor="meter_thirst">
        <img src="/thirst.png" width="30" height="30" />
      </label>
      &nbsp; &nbsp;
      <meter id="meter_thirst" value={result.thirst} min="-1" max="1"></meter>
      <br />
      <label htmlFor="meter_exhaustion">
        <img src="/exhaustion.png" width="30" height="30" />
      </label>
      &nbsp; &nbsp;
      <meter
        id="meter_exhaustion"
        value={result.exhaustion}
        min="-1"
        max="1"
      ></meter>
      <br />
      <label htmlFor="meter_happiness">
        <img src="/happiness.png" width="30" height="30" />
      </label>
      &nbsp; &nbsp;
      <meter
        id="meter_happiness"
        value={result.happiness}
        min="-1"
        max="1"
      ></meter>
    </div>
  );
};
function Result(props) {
  let [result, setResult] = useState(defaultResults[props.result]);
  useEffect(() => {
    fetchAPI(props.path).then((data) => {
      setResult(data);
    });
  }, []);

  switch (props.result) {
    case "pose":
      return handlePose(result);
    case "color-image":
    case "depth-image":
      let url = formatURL(`${props.path}/data`);
      return handleImage(url);
    case "feelings":
      return handleFeelings(result);
  }
}

function Post(props) {
  let [results, setResults] = useState([]);
  let path = `/users/${props.userId}/snapshots/${props.snapshotId}`;
  useEffect(() => {
    fetchAPI(path).then((data) => {
      setResults(data.results);
    });
  }, []);

  let resultsList = [];
  results.forEach(function (result) {
    let path = `/users/${props.userId}/snapshots/${props.snapshotId}/${result}`;
    let collapse = <Result path={path} result={result} />;
    resultsList.push(collapse);
  });

  let date = showTimestamp(props.datetime);
  return (
    <div>
      <h1>#{props.snapshotId}</h1>
      <h3>{date}</h3>
      {resultsList}
    </div>
  );
}

function Posts(props) {
  let [snapshots, setSnapshots] = useState([]);
  useEffect(() => {
    fetchAPI(`/users/${props.userId}/snapshots`).then((data) => {
      setSnapshots(data);
    });
  }, []);

  let posts = [];
  snapshots.forEach((snapshot) => {
    posts.push(
      <div className="post">
        <Post
          userId={props.userId}
          snapshotId={snapshot.uuid}
          datetime={snapshot.datetime}
        />
      </div>
    );
  });
  return <div>{posts}</div>;
}

function UserPage(props) {
  let match = props.match;
  let userId = match.params.id;

  let [user, setUser] = useState({});
  useEffect(() => {
    fetchAPI(`/users/${userId}`).then((data) => {
      let firstLastName = data.username.split(" ");
      let initials = firstLastName[0][0] + firstLastName[1][0];
      setUser({
        username: data.username,
        birthday: data.birthday,
        gender: data.gender,
        initials: initials,
      });
    });
  }, []);

  let birthday = showTimestamp(user.birthday);

  return (
    <div className="usersPage">
      <div className="profile">
        <div className="userImage">{user.initials}</div>
        <h2 className="userNameText">{user.userName}</h2>
        <div>
          <span className="userDetail">User ID: {userId}</span>
          <span className="userDetail">Birthday: {birthday}</span>
          <span className="userDetail">Gender: {user.gender}</span>
        </div>
      </div>
      <div className="posts">
        <Posts userId={userId} />
      </div>
    </div>
  );
}

export default UserPage;

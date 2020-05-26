import React, { useState, useEffect } from "react";
import "../css/user-page.css";
import { fetchAPI, showTimestamp, formatURL } from "../utils";

class ShowImages extends React.Component {
  constructor(props) {
    super(props);
    this.state = { clickState: false };
    this.handleClick = this.handleClick.bind(this);
  }
  render() {
    let src = this.state.clickState
      ? this.props.depthImage
      : this.props.colorImage;
    return (
      <div className="view overlay">
        <img src={src} className="img-fluid" />
        <a>
          <div
            className="mask rgba-white-slight"
            onClick={this.handleClick}
          ></div>
        </a>
      </div>
    );
  }
  handleClick() {
    this.setState({ clickState: !this.state.clickState });
  }
}

function ShowPose(props) {
  let url = props.url;
  let [pose, setPose] = useState({
    translation: { x: 0, y: 0, z: 0 },
    rotation: { x: 0, y: 0, z: 0, w: 0 },
  });
  useEffect(() => {
    fetchAPI(url).then((data) => {
      setPose(data);
    });
  }, []);

  let [translation, rotation] = [pose.translation, pose.rotation];
  let [tx, ty, tz] = [translation.x, translation.y, translation.z];
  let [rx, ry, rz, rw] = [rotation.x, rotation.y, rotation.z, rotation.w];
  return (
    <div className="results-pose">
      <h5>Pose</h5>
      <p className="tab">
        translation
        <ul className="tab">
          <li>x: {tx}</li>
          <li>y: {ty}</li>
          <li>z: {tz}</li>
        </ul>
        rotation
        <ul className="tab">
          <li>x: {rx}</li>
          <li>y: {ry}</li>
          <li>z: {rz}</li>
          <li>w: {rw}</li>
        </ul>
      </p>
    </div>
  );
}

function ShowFeelings(props) {
  let url = props.url;
  let [feelings, setFeelings] = useState({
    hunger: 0,
    thirst: 0,
    exhaustion: 0,
    happiness: 0,
  });
  useEffect(() => {
    fetchAPI(url).then((data) => {
      setFeelings(data);
    });
  }, []);

  let progress_bars = {};
  for (let feeling in feelings) {
    let value = feelings[feeling];
    let cname = "bg-success";
    if (-0.5 < value && value <= 0) cname = "bg-info";
    else if (0 < value && value <= 0.5) cname = "bg-warning";
    else if (0.5 < value && value <= 1) cname = "bg-danger";
    let normalized = value * 50 + 50;
    let pbar = (
      <div className="progress md-progress feelings-progress-bar">
        <div
          className={`progress-bar ${cname}`}
          role="progressbar"
          style={{ width: `${normalized}%` }}
          aria-valuenow={normalized.toString()}
          aria-valuemin="0"
          aria-valuemax="100"
        >
          {value}
        </div>
      </div>
    );
    progress_bars[feeling] = pbar;
  }
  return (
    <div className="results-feelings">
      <h5>Feelings</h5>
      <p className="tab">
        hunger: {progress_bars.hunger} <br />
        thirst: {progress_bars.thirst} <br />
        exhaustion: {progress_bars.exhaustion} <br />
        happiness: {progress_bars.happiness}
      </p>
    </div>
  );
}

function Snapshot(props) {
  let userId = props.userId;
  let username = props.username;
  let snapshotId = props.snapshotId;
  let domId = `snapshot-${userId}-${snapshotId}`;
  let datetime = showTimestamp(props.datetime);

  let snapshotUrl = `/users/${userId}/snapshots/${snapshotId}`;

  let [details, setDetails] = useState({ results: [] });
  let [moreDetails, setMoreDetails] = useState(false);
  let handleMoreDetails = () => {
    setMoreDetails(!moreDetails);
  };
  useEffect(() => {
    fetchAPI(snapshotUrl).then((data) => {
      setDetails({ results: data.results });
    });
  }, []);

  let colorImage = details.results.includes("color_image")
    ? formatURL(`${snapshotUrl}/color_image/data`)
    : "";
  let depthImage = details.results.includes("depth_image")
    ? formatURL(`${snapshotUrl}/depth_image/data`)
    : "";

  let pose = "";
  if (details.results.includes("pose") && moreDetails)
    pose = <ShowPose url={`${snapshotUrl}/pose`} />;
  let feelings = "";
  if (details.results.includes("feelings") && moreDetails)
    feelings = <ShowFeelings url={`${snapshotUrl}/feelings`} />;
  let resultsItems = [];
  let brs = [<br />, <br />, <br />, <br />];
  details.results.forEach((item) => {
    resultsItems.push(<li>{item}</li>);
    brs.pop();
  });
  let colorImageView = "";
  let depthImageView = "";
  if (moreDetails) {
    colorImageView = (
      <ShowImages colorImage={colorImage} depthImage={depthImage} />
    );
    depthImageView = (
      <img
        src={formatURL(`${snapshotUrl}/depth_image/data`)}
        className="img-fluid"
      />
    );
  }

  return (
    <div className="snapshot-container">
      <div className="jumbotron text-center hoverable p-4 snapshot">
        <div className="row">
          <div className="col-md-7 text-md-left ml-3 mt-3">
            <h4 className="h4 mb-4">Snapshot #{snapshotId}</h4>
            <p className="font-weight-normal">
              by{" "}
              <a>
                <strong>{username}</strong>
              </a>
              , {datetime}
            </p>
            Available results:
            <ul>{resultsItems}</ul>
            {brs}
            <div>
              <button
                className="btn aqua-gradient"
                type="button"
                data-toggle="collapse"
                data-target={`#collapse-${domId}`}
                aria-expanded="false"
                aria-controls={`collapse-${domId}`}
                onClick={handleMoreDetails}
              >
                {moreDetails ? (
                  <span>
                    Hide results <i className="fas fa-angle-double-up"></i>
                  </span>
                ) : (
                  <span>
                    Show results <i className="fas fa-angle-double-down"></i>
                  </span>
                )}
              </button>
            </div>
            <div className="collapse" id={`collapse-${domId}`}>
              <div className="mt-3">
                {pose}
                {feelings}
              </div>
            </div>
          </div>
          <div className="col-md-4 offset-md-1 mx-3 my-3">
            <div className="collapse" id={`collapse-${domId}`}>
              {colorImageView}
              <div className="mt-3">
                <div className="view overlay">
                  {depthImageView}
                  <a>
                    <div className="mask rgba-white-slight"></div>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function UserSnapshots(props) {
  let userId = props.userId;
  let [snapshots, setSnapshots] = useState([]);

  useEffect(() => {
    fetchAPI(`/users/${userId}/snapshots`).then((data) => {
      setSnapshots(data);
    });
  }, []);

  let snapshotViews = [];
  snapshots.forEach((snapshot) => {
    snapshotViews.push(
      <Snapshot
        userId={userId}
        username={props.username}
        snapshotId={snapshot.uuid}
        datetime={snapshot.datetime}
      />
    );
  });

  return <div className="user-snapshots">{snapshotViews}</div>;
}

export default UserSnapshots;

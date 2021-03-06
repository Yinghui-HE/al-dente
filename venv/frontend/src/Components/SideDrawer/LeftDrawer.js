import React, { useState, useEffect } from "react";
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import CssBaseline from '@material-ui/core/CssBaseline';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
//import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';

import Dashboard from "../../Dashboard.js"
import UserProfile from "../../UserProfile.js"
import Followers from "../../Followers.js"
import { BrowserRouter, Route, Redirect } from 'react-router-dom';
import { useHistory } from "react-router-dom";

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  appBar: {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: drawerWidth,
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  // necessary for content to be below app bar
  toolbar: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
  },
}));

export default function LeftDrawer(props) {
  const classes = useStyles();
  const [profileRedirect, setProfileRedirect] = useState(false);
  const [dashboardRedirect, setDashboardRedirect] = useState(false);
  const [followersRedirect, setFollowersRedirect] = useState(false);

  const [userInfo, setUserInfo] = useState({});
  const [currLocation, setCurrLocation] = useState("");

  const [nextAddress, setNextAddress] = useState("");
  console.log("drawer props:", props);

  let history = useHistory();
  console.log("history:", history);

  useEffect(() => {
    setUserInfo(props.userInfo);
    setCurrLocation(props.currLocation);
  }, [props.userInfo, props.currLocation]);

  function handleDrawerOnclick(address) {
    setNextAddress(address.text);
    console.log("next address:", nextAddress);
    console.log("drawer props:", props);

    if (nextAddress === "Profile") {
        setProfileRedirect(true);
        console.log("equal profile");
//        history.push({
//            pathname: '/profile',
//            state: {
//                from: currLocation,
//                userInfo: userInfo
//            }
//        });
    } else if (nextAddress === "Dashboard") {
        setDashboardRedirect(true);
        console.log("equal dashboard");
    } else if (nextAddress === "Following") {
        setFollowersRedirect(true);
        console.log("equal followers");
    }
    console.log("no equal");
  }


  return (
    profileRedirect ?
    (
        <BrowserRouter>
            <Route path = '/profile'
                render = {props => <UserProfile {...props} data={userInfo} />} />
            <Redirect to={{ pathname: '/profile', state: {from: currLocation}}}/>
        </BrowserRouter>
    ) :
    dashboardRedirect ?
    (
        <BrowserRouter>
            <Route path = '/dashboard'
                render = {props => <Dashboard {...props} data={userInfo} />} />
            <Redirect to={{ pathname: '/dashboard', state: {from: currLocation}}} />
        </BrowserRouter>
    ) :
    followersRedirect ?
    (
        <BrowserRouter>
            <Route path = '/following'
                render = {props => <Followers {...props} data={userInfo} />} />
            <Redirect to={{ pathname: '/following', state: {from: currLocation}}} />
        </BrowserRouter>
    ) :
    (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar position="fixed" className={classes.appBar}>
        <Toolbar>
          <Typography variant="h5" noWrap>
            al dente
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        className={classes.drawer}
        variant="permanent"
        classes={{
          paper: classes.drawerPaper,
        }}
        anchor="left"
      >
        <div className={classes.toolbar} />
        <Divider />
        <List>
          {['Dashboard', 'Profile', 'Following', 'Maps'].map((text, index) => (
            <ListItem button key={text} onClick={ () => handleDrawerOnclick({text})}>
              <ListItemText primary={text} />
            </ListItem>
          ))}
        </List>
      </Drawer>
    </div>)
  );
}

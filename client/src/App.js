import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import Index from './components/pages/Index';
import TopicsSearch from './components/pages/TopicsSearch';
import TopicShow from './components/pages/TopicShow';

const App = () => (
  <Router>
    {/* <nav>
        <ul>
        <li>
        <Link to="/">Home</Link>
        </li>
        </ul>
        </nav> */}

    <Route path="/" exact component={Index} />
    <Route path="/topics" exact component={TopicsSearch} />
    <Route path="/topics/:topicId" exact component={TopicShow} />
  </Router>
);


export default App;

import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { HelmetProvider, Helmet } from 'react-helmet-async';

import Index from './components/pages/Index';
import TopicsSearch from './components/pages/TopicsSearch';
import TopicShow from './components/pages/TopicShow';
import Verses from './components/pages/Verses';
import About from './components/pages/About';

import Navigation from './components/Navigation';

const App = () => (
  <HelmetProvider>
    <Helmet>
      <title>Ecce - Bible Explorer</title>
    </Helmet>

    <Router>
      <Navigation />

      <Route path="/" exact component={Index} />
      <Route path="/about" exact component={About} />
      <Route path="/verses" exact component={Verses} />
      <Route path="/topics" exact component={TopicsSearch} />
      <Route path="/topics/:topicId" exact component={TopicShow} />
    </Router>
  </HelmetProvider>
);


export default App;

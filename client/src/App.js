import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { HelmetProvider, Helmet } from 'react-helmet-async';

import Index from './components/page/Index';
import TopicsSearch from './components/page/TopicsSearch';
import TopicShow from './components/page/TopicShow';
import Verses from './components/page/Verses';
import Eda from './components/page/Eda';

import Navigation from './components/Navigation';
import Footer from './components/Footer';

const App = () => (
  <HelmetProvider>
    <Helmet>
      <title>Ecce - Bible Explorer</title>
    </Helmet>

    <Router>
      <div className="flex flex-col min-h-screen">
        <Navigation />

        <div className="flex-grow">
          <Route path="/" exact component={Index} />
          <Route path="/verses" exact component={Verses} />
          <Route path="/topics" exact component={TopicsSearch} />
          <Route path="/topics/:topicId" exact component={TopicShow} />
          <Route path="/eda" exact component={Eda} />
        </div>
        <Footer />
      </div>
    </Router>
  </HelmetProvider>
);


export default App;

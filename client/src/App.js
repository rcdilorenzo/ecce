import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import Index from './components/pages/Index';

const App = () => (
  <Router>
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
      </ul>
    </nav>

    <Route path="/" exact component={Index} />
  </Router>
);


export default App;

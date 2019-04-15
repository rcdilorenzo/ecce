import React from 'react';
import { Link } from 'react-router-dom';

const RealSearchResult = ({ id, label, reference_count, placeholder }) => (
  <Link to={`/topics/${id}`} className="search-result-link">
    <header className="search-result-link__title">{label}</header>
    <p className="search-result-link__details">{reference_count} Verses</p>
  </Link>
);

const PlaceholderSearchResult = _props => (
  <div>
    <header className="italic">Loading</header>
  </div>
);

const TopicSearchResult = (props) => {
  if (props.placeholder) {
    return <PlaceholderSearchResult {...props} />;
  } else {
    return <RealSearchResult {...props} />;
  }
 };

export default TopicSearchResult;

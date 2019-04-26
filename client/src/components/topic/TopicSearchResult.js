import React from 'react';
import { Link } from 'react-router-dom';

const RealSearchResult = ({ id, label, reference_count, openNewTab }) => (
  <Link
    to={`/topics/${id}`}
    target={openNewTab ? '_blank' : null}
    className={ reference_count ? "list-item" : "list-item list-item--inline" }>

    <header className="list-item__title">{label}</header>
    {reference_count &&
     <p className="list-item__details">
       {reference_count} verses
     </p>}

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

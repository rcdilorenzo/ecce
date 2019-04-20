import React, { Component } from 'react';

class Card extends Component {
  constructor(props) {
    super(props);

    this.className = [
      'flex-1',
      'flex-no-shrink',
      'mt-4',
      'mb-4',
      'p-8',
      'bg-grey-subtle',
      'rounded-lg',
      'shadow-md',
      'card'
    ].join(' ');

    this.state = { isLoaded: props.waitForLoad || false };
  }

  componentDidMount() {
    this.setState({ isLoaded: true });
  }

  render() {
    return (
      <div className={this.className}>
        {this.state.isLoaded && this.props.children}
      </div>
    );
  }
}

export default Card;

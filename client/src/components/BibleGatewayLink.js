import React from 'react';

export const READ_MORE_STYLE = 'READ_MORE_STYLE'

const classNameForStyle = style => {
  if (style === READ_MORE_STYLE) {
    return 'text-black uppercase pt-3 text-xs no-underline float-left';
  }
  return '';
};

const BibleGatewayLink = ({ passage, children, className, style, text }) => (
  <a className={(className || '') + classNameForStyle(style)}
    href={`https://www.biblegateway.com/passage/?search=${passage.name}&version=ESV`}
    target={'_blank'}>
    {text}
    {!text && children}
  </a>
);

export default BibleGatewayLink;

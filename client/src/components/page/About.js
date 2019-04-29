import React from 'react';
import { Helmet } from 'react-helmet-async';

import PageWrapper from '../PageWrapper';

const Content = _props => (
  <main className="content">
    <h1>About</h1>
    <img
      style={{ borderRadius: '50%', maxWidth: '120px' }}
      className="mx-auto block mt-2 mb-3"
      src="https://www.gravatar.com/avatar/781722c6af940e41c2a546565dd9ff7e?s=512&amp;d=mm&amp;r=x" />
    <p>
      My name is Christian Di Lorenzo. I am a young yet highly-motivated software practitioner with experience in several technology spaces including native iOS development, full-stack web apps, and Data Science. I have a B.S. in Computer Science and an M.S. in Data Science from Regis University. I have worked at RoleModel Software since graduating from their first <a href="http://craftsmanshipacademy.com/">Software Craftsmanship Academy</a> in 2012.
    </p>
    <p>
      I'm not simply content to solve difficult problems. I love to push the possibilities of sustainable software to discover and implement new methodologies such as blending Domain-Driven Design (DDD) and Functional Programming (FP) with the best practices of Object-Oriented Programming (OOP).
    </p>
    <p>
      My expertise resides in a variety of languages, technologies, and methodologies:
    </p>
    <ul>
      <li>Swift, Objective-C, CoreData, and AFNetworking</li>
      <li>Ruby on Rails</li>
      <li>ReactJS, ES6+, RamdaJS, and NodeJS</li>
      <li>Elixir, Phoenix, and Ecto</li>
      <li>HTML and CSS</li>
      <li>Python and R</li>
      <li>Pandas, Numpy, Keras, Tensorflow, and Matplotlib</li>
      <li>Data Visualization with Python, JavaScript, R, and Tableau</li>
      <li>Statistics, Machine Learning, Category Theory, …</li>
    </ul>
    <p>
      Aside from projects like this one, I occasionally write for my new blog <a href="https://rcd.ai">Rcd.AI</a>. I also contribute to several open source libraries such as <a href="https://github.com/rcdilorenzo/filtrex">filtrex</a> which has close to 30,000 downloads. Feel free to check out my <a href="https://github.com/rcdilorenzo">GitHub profile</a>. I also love design and am always eager to provide accommodating and thoughtful user experiences.
    </p>
    <p>
      Aside from technical things, I actively participate in my church as well as play the accordion, piano, or saxophone whenever the opportunity arises. I currently live at home and tutor math to my three younger siblings in their homeschool journey. In my free time, I enjoy ultimate frisbee with family, friends, and even competitive athletes.
    </p>
</main>
);

const About = _props => (
  <PageWrapper>
    <Helmet>
      <title>Ecce - About</title>
    </Helmet>

    <Content />
  </PageWrapper>
);


export default About;

import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';

import store from './store'
import Sample from './components/sample.jsx';

ReactDOM.render(
    <Provider store={store}>
        <Sample/>
    </Provider>, document.getElementById('its-a-draw')
);

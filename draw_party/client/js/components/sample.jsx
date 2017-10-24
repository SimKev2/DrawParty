import React from 'react';
import { connect } from 'react-redux';

const getStyle = function(passedinvalue){
    return {
        color: (passedinvalue === 'sampleStoreValue') ? 'green' : 'blue'
    };
};

@connect((store) => {
    return {
        someStoreValue: store.someStoreValue
    };
})
export default class Sample extends React.Component{
    render() {
        return (
            <div style={getStyle(this.props.someStoreValue)}>
                Yo dis lit, fam
            </div>
        );
    }
};

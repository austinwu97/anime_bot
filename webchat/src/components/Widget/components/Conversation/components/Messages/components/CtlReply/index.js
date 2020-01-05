import React, { PureComponent } from 'react';
import { PROP_TYPES } from 'constants';

import './styles.scss';

class CtlReply extends PureComponent {
  render() {
   
    // Convert map to object
    const message = [...this.props.message.entries()].reduce( (acc, e) => ( 
      acc[e[0]] = e[1], 
      acc), {});
    var { background_url } = message;
    
    console.log("in CtlReply=" + message);

 //   if (background_url !== undefined) {
  //      const body = document.getElementsByTagName('body')[0];
  //      body.style.backgroundImage = ''.concat("url('", background_url, "')");
 //   }

    return (
      <div className="control">
        <div className="control-details">
        </div>
      </div>
    );
  }
}

CtlReply.propTypes = {
  message: PROP_TYPES.CTLREPLY
};

CtlReply.defaultProps = {
  params: {}
}

export default CtlReply;

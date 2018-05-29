import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Button } from 'react-native-elements';

const styles = StyleSheet.create({
  container: {

  },
  button: {
    backgroundColor: '#F8CA0D',
    borderRadius: 12
  }
});

class CloseButton extends React.Component{

  closeLock = () => {
    
  }

  render(){
    return(
      <View style={styles.container}>
        <Button
          title='Cerrar cerradura'
          icon={{name:'lock', color: '#000'}}
          color='#000'
          buttonStyle={styles.button}
          containerViewStyle={styles.button}
          onPress={this.closeLock}
        />
      </View>
    );
  }
}

export default CloseButton;
import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Button } from 'react-native-elements';

const styles = StyleSheet.create({
  container: {
    marginVertical: 16
  },
  button: {
    backgroundColor: '#F8CA0D',
    borderRadius: 12
  }
});

class OpenButton extends React.Component{

  openLock = () => {
    
  }

  render(){
    return(
      <View style={styles.container}>
        <Button
          title='Abrir cerradura'
          icon={{name:'lock-open', color: '#000'}}
          color='#000'
          buttonStyle={styles.button}
          onPress={this.openLock}
        />
      </View>
    );
  }
}

export default OpenButton;
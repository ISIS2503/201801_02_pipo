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

class OpenButton extends React.Component {

  openLock = () => {
    fetch('http://ec2-34-202-239-178.compute-1.amazonaws.com:8080/cerradura/abrir', {
      method: 'PUT'
    }).then((response) => {
      ToastAndroid.show('Cerradura abriéndose', ToastAndroid.LONG);
      console.log(response)
    });
  }

  render() {
    return (
      <View style={styles.container}>
        <Button
          title='Abrir cerradura'
          icon={{ name: 'lock-open', color: '#000' }}
          color='#000'
          buttonStyle={styles.button}
          onPress={this.openLock}
        />
      </View>
    );
  }
}

export default OpenButton;
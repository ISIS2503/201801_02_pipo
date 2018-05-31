import React from 'react';
import { View, Text, StyleSheet, TextInput, ToastAndroid } from 'react-native';
import { Button } from 'react-native-elements';

const styles = StyleSheet.create({
  container: {
    paddingTop: 16
  },
  title: {
    fontSize: 20,
    borderBottomColor: '#F8CA0D',
    borderBottomWidth: 2
  },
  inputContainer: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-between',
    /* alignItems:'center', */
    paddingTop: 8
  },
  input: {
    height: 40,
    width: 184,
    fontSize: 28,
    textAlign: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#F8CA0D'
  },
  button: {
    backgroundColor: '#F8CA0D',
    borderRadius: 8
  }
});


class InsertPassword extends React.Component {

  constructor() {
    super();
    this.state = {
      clave: ''
    }
  }

  sendPassword = () => {
    fetch('http://ec2-34-202-239-178.compute-1.amazonaws.com:8080/unidadesResidenciales/Toscana/inmuebles/2-5-3/hub/cerradura/gestionClaves', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "combinacion": this.state.clave,
        "indice": 0
      })
    }).then((response) => {
      ToastAndroid.show('Clave "' + this.state.clave + '" enviada', ToastAndroid.SHORT);
      this.setState({
        clave: ''
      })
      console.log(response)
    });
  }

  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Ingresar nueva clave</Text>
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder='Nueva clave'
            underlineColorAndroid='#0000'
            onChangeText={(clave) => this.setState({ clave })}
            maxLength={4}
            keyboardType='numeric'
            value={this.state.clave}
          />
          <Button
            title='Enviar'
            icon={{ name: 'cloud-upload', color: '#000' }}
            large
            color='#000'
            buttonStyle={styles.button}
            onPress={this.sendPassword}
            disabled={this.state.clave.length != 4}
          />
        </View>
      </View>
    );
  }
}

export default InsertPassword;
import React from 'react';
import { View, Text, StyleSheet, TextInput, ToastAndroid } from 'react-native';
import { Button } from 'react-native-elements';
import DatePicker from 'react-native-datepicker';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'space-between',
    flexDirection: 'column',
    paddingTop: 40
  },
  title: {
    fontSize: 20,
    borderBottomColor: '#F8CA0D',
    borderBottomWidth: 2
  },
  pickers: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingTop: 8,
    width: '100%'
  },
  pickerContainer: {
    height: 80,
    width: '50%'
  },
  picker: {
    width: '100%'
  },
  button: {
    backgroundColor: '#F8CA0D',
    borderRadius: 8
  }
});


class InsertSchedule extends React.Component {

  constructor() {
    super();
    this.state = {
      schedule_start: null,
      schedule_end: null
    }
  }

  sendSchedule = () => {
    fetch('http://ec2-34-202-239-178.compute-1.amazonaws.com:8080/unidadesResidenciales/Toscana/inmuebles/2-5-3/hub/cerradura/horariosPermitidos', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        horaInicio: this.state.schedule_start,
        horaFin: this.state.schedule_end
      })
    }).then((response) => {
      ToastAndroid.show('Horario enviado', ToastAndroid.SHORT);
      this.setState({
        schedule_end : null,
        schedule_start: null
      });
      console.log(response);
    }).catch(error => {
      ToastAndroid.show('Error enviando el horario: ' + error);
      console.log(error);
    });
  }

  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Ingresar un nuevo horario permitido</Text>
        <View style={styles.pickers}>
          <View style={styles.pickerContainer}>
            <Text>Hora de inicio</Text>
            <DatePicker
              style={styles.picker}
              date={this.state.schedule_start}
              mode="time"
              placeholder="Seleccionar un horario"
              onDateChange={date => this.setState({ schedule_start: date })}
            />
          </View>
          <View style={styles.pickerContainer}>
            <Text>Hora de fin</Text>
            <DatePicker
              style={styles.picker}
              date={this.state.schedule_end}
              mode="time"
              placeholder="Seleccionar un horario"
              onDateChange={date => this.setState({ schedule_end: date })}
            />
          </View>
        </View>
        <View style={{ position: 'absolute', top: '40%', width: '100%' }}>
          <Button
            title='Enviar horario'
            icon={{ name: 'alarm', color: '#000' }}
            color='#000'
            buttonStyle={styles.button}
            containerViewStyle={styles.button}
            disabled={!(this.state.schedule_start && this.state.schedule_end)}
            onPress={this.sendSchedule}
          />
        </View>
      </View>
    );
  }
}

export default InsertSchedule;
import React from 'react';
import { StyleSheet, Text, View, Image, StatusBar } from 'react-native';

import CloseButton from './components/CloseButton';
import OpenButton from './components/OpenButton';
import InsertPassword from './components/InsertPassword';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'flex-start',
    backgroundColor: '#FEFEFA',
    paddingTop: 16,
    paddingHorizontal: 16
  },
  logoContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-start',
  },
  logo: {
    height: 80,
    width: 80
  },
  title: {
    paddingLeft: 8,
    fontSize: 28
  },
  contentContainer: {
    flex: 6
  }
});

class App extends React.Component {
  render() {
    return (
      <View style={styles.container}>
        <StatusBar hidden={true} />
        <View style={styles.logoContainer}>
          <Image
            source={require('./assets/yale.png')}
            style={styles.logo}
          />
          <Text style={styles.title}> <Text style={{ fontSize: 38 }}>π</Text>po App </Text>
        </View>
        <View style={styles.contentContainer}>
          <OpenButton />
          <CloseButton />
          <InsertPassword />
        </View>
      </View>
    );
  }
}

export default App;

export async function injectDice(pyodide) {
  const dice = await (await fetch('dice.py')).text();
  pyodide.FS.writeFile('/home/pyodide/dice.py', dice);
  pyodide.runPython('from dice import *');
}
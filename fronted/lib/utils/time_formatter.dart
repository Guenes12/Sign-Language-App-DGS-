String formatTime(int seconds) {

 final min = (seconds ~/ 60)
     .toString()
     .padLeft(2, '0');
 final sec = (seconds % 60)
     .toString()
     .padLeft(2, '0');
 return "$min:$sec";
 
}
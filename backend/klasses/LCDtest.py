from LCD import LCDcontrol


scherm = LCDcontrol(17, 5, 6, 13, 19, 26, 21, 20, 27, 22)
scherm.init_screen([1,1,0], [1,0,0])
scherm.clear_display()
scherm.show_ip()
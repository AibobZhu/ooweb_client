from ooweb_client.components_client import *


def create_demo_page():
    with WebPage(name='mypage', value='<OwwwO>') as page:
        with page.add_child(WebRow()) as r1:
            with r1.add_child(WebColumn( width=['md6'], offset=['mdo3'], align=['horizon-center'])) as r1c1:
                with r1c1.add_child(WebHead1(value='&lt;OwwwO&gt; 	 Demo')) as h1:
                    pass
        with page.add_child(WebRow(height='400px')) as r2:
            with r2.add_child(WebColumn(height='100%', width=['md2'], offset=['mdo3'])) as r2c1:
                with r2c1.add_child(WebField(value='左控件')) as r2c1fs:
                    with r2c1fs.add_child(WebImg(value='img/burns.jpg', align=['horizon-center'])) as r2c1img:
                        pass
            with r2.add_child(WebColumn(height='100%', width=['md4'])) as r2c2:
                with r2c2.add_child(WebField(value='右控件')) as r2c2fs:
                    with r2c2fs.add_child(WebImg(value='img/bobdylen.jpg', align=['horizon-center'])) as r2c2img:
                        pass
        with page.add_child(WebBr()):
            pass
        with page.add_child(WebRow()) as r3:
            with r3.add_child(WebColumn(width=['md6'], offset=['mdo3'], align=['horizon-center'])) as r3c1:
                with r3c1.add_child(WebBtnToggle(value='左2右4')) as r3c1btn:
                    with r3c1btn.on_click():
                        r3c1btn.toggle()
                        with r3c1btn.if_():
                            with r3c1btn.condition():
                                r2c1.is_width('md2')
                            with r3c1btn.cmds():
                                r2c1.remove_width('md2')
                                r2c1.set_width('md4')
                                r2c2.remove_width('md4')
                                r2c2.set_width('md2')
                                r3c1btn.value('左4右2')
                        with r3c1btn.else_():
                            with r3c1btn.cmds():
                                r2c1.remove_width('md4')
                                r2c1.set_width('md2')
                                r2c2.remove_width('md2')
                                r2c2.set_width('md4')
                                r3c1btn.value('左2右4')

    return page.render()

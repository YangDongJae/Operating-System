import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

form_class = uic.loadUiType("os.ui")[0]


class Process:
    def __init__(self, process_id: int, arrival_time: int, burst_time: int):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.color = None


class ProcessScheduler:
    def __init__(self):
        self.processes = []

    def add_process(self, process_id: int, arrival_time: int, burst_time: int, color: QColor):
        process = Process(process_id, arrival_time, burst_time)
        process.color = color
        self.processes.append(process)
        self.print_processes()

    def remove_process(self, process_id: int):
        self.processes = [
            process for process in self.processes if process.process_id != process_id]
        self.print_processes()

    def get_process_color(self, process_id: str):
        for process in self.processes:
            if process.process_id == process_id:
                return process.color
        return None
    
    def get_processes_length(self):
        return len(self.processes)

    def print_processes(self):
        print("Process List:")
        for process in self.processes:
            print(
                f"Process ID: {process.process_id}, Arrival Time: {process.arrival_time}, Burst Time: {process.burst_time}")


class OS_Scheduler(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        # 코어 개수 설정
        self.core = [0] * 4
        # 추가하는 프로세서 이름, AT, BT
        self.addProcessName = 1
        self.addArrivalTime = 0
        self.addBurstTime = 0

        self.existing_colors = []

        # selected = 클릭한 model과 complex, gpt_model, gpt_complex = 최종 결정한 결과
        # model : 3.5 = 1, 4.0 = 2, complex : high = 9, mid = 5, low = 1
        self.gpt_selected = []
        self.gpt_model = self.gpt_complex = -1

        self.setupUi(self)
        self.setWindowTitle('OS Scheduler')
        self.setWindowIcon(QIcon('logo/logo.png'))
        self.lb_core.setText(
            f"현재 코어: P-Core : {self.core.count(1)}개, E-Core : {self.core.count(2)}개")
        self.move(300, 300)
        self.resize(1920, 1080)
        # self.setFixedSize(1920, 1080)
        self.scheduler = ProcessScheduler()

        self.pb_model1.setCheckable(True)
        self.pb_model2.setCheckable(True)

        self.pb_high.setCheckable(True)
        self.pb_mid.setCheckable(True)
        self.pb_low.setCheckable(True)

        self.gb_Timeq.setVisible(False)
        self.pb_remove.setVisible(False)

        # column 너비 변경 불가능
        self.tw_process.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        # 알고리즘 선택 기능 연결
        # cb => algorithm : 1, core 0~3 : 2~5
        self.cb_algorithm.currentIndexChanged.connect(
            lambda: self.comboBoxFunction(1, self.cb_algorithm.currentIndex()))
        for i in range(4):
            combobox = getattr(self, 'cb_core{}'.format(i))
            combobox.currentIndexChanged.connect(
                lambda index, i=i: self.comboBoxFunction(i + 2, index))

        # GPT 모델 선택 기능 연결
        self.pb_model1.clicked.connect(lambda: self.GPTSelectFunction(1))
        self.pb_model2.clicked.connect(lambda: self.GPTSelectFunction(2))

        self.pb_high.clicked.connect(lambda: self.GPTSelectFunction(3))
        self.pb_mid.clicked.connect(lambda: self.GPTSelectFunction(4))
        self.pb_low.clicked.connect(lambda: self.GPTSelectFunction(5))

        # 프로세스 추가, 삭제 기능 연결
        for i in range(3):
            pb_up = getattr(self, 'pb_up{}'.format(i+1))
            pb_down = getattr(self, 'pb_down{}'.format(i+1))
            pb_up.clicked.connect(
                (lambda index: lambda: self.processAddFunction(index*2+1))(i))
            pb_down.clicked.connect(
                (lambda index: lambda: self.processAddFunction(index*2+2))(i))
        self.pb_resetp.clicked.connect(lambda: self.processAddFunction(7))
        self.pb_savep.clicked.connect(lambda: self.processAddFunction(8))
        self.tw_process.itemSelectionChanged.connect(
            lambda: self.rbVisibilityFunction())
        self.pb_remove.clicked.connect(lambda: self.processRemoveFunction())
        self.pb_random.clicked.connect(lambda: self.RandomAddProcessFunction())

        # 메뉴 기능 연결
        self.a_exit.triggered.connect(QApplication.exit)

    # 프로세스 이름 최신화    
    def updateProcessNameFunction(self):
        self.addProcessName = self.scheduler.get_processes_length() + 1
        self.lb_add_process.setText(f"P{self.addProcessName:02}")

    # 프로세스 추가
    def processAddFunction(self, flag):
        if flag == 1:  # Name up
            self.addProcessName += 1
            self.lb_add_process.setText(f"P{self.addProcessName:02}")
        elif flag == 2:  # Name down
            if self.addProcessName > 1:
                self.addProcessName -= 1
            self.lb_add_process.setText(f"P{self.addProcessName:02}")
        elif flag == 3:  # AT up
            self.addArrivalTime += 1
            self.lb_add_process_at.setText(f"{self.addArrivalTime:02}")
        elif flag == 4:  # AT down
            if self.addArrivalTime > 0:
                self.addArrivalTime -= 1
            self.lb_add_process_at.setText(f"{self.addArrivalTime:02}")
        elif flag == 5:  # BT up
            self.addBurstTime += 1
            self.lb_add_process_bt.setText(f"{self.addBurstTime:02}")
        elif flag == 6:  # BT down
            if self.addBurstTime > 0:
                self.addBurstTime -= 1
            self.lb_add_process_bt.setText(f"{self.addBurstTime:02}")
        elif flag == 7:  # reset
            self.updateProcessNameFunction()
            self.addArrivalTime = 0
            self.addBurstTime = 0
            self.lb_add_process_at.setText(f"{self.addArrivalTime:02}")
            self.lb_add_process_bt.setText(f"{self.addBurstTime:02}")
        elif flag == 8:  # save
            pid = self.addProcessName
            at = self.addArrivalTime
            bt = self.addBurstTime

            # 이미 동일한 pid가 processes에 있는지 확인
            pid_exists = any(process.process_id ==
                             pid for process in self.scheduler.processes)
            # # arrival_time이 동일한 프로세스가 있는지 확인
            # same_at_exists = any(process.arrival_time == at for process in self.scheduler.processes)

            if pid_exists:
                QMessageBox.warning(self, '추가 실패', f'프로세스 {pid}는 이미 존재합니다.')
            # elif same_at_exists:
            #     QMessageBox.warning(self, '추가 실패', f'도착 시간 {at}와 동일한 도착 시간을 가진 프로세스가 이미 존재합니다.')
            elif int(bt) <= 0:
                QMessageBox.warning(self, "추가 실패", "Burst Time은 0일 수 없습니다.")
            else:
                self.createProcessFunction(pid, at, bt)
                self.updateProcessNameFunction()

    # 랜덤 프로세스 추가
    # model : 3.5 = 1, 4.0 = 2, complex : high = 9, mid = 5, low = 1
    def RandomAddProcessFunction(self, is_DRR = False):
        if is_DRR:
            i = self.scheduler.get_processes_length() + 1
            # print(f"i = {i}, length = {self.scheduler.get_processes_length()}")
            for _ in range(3):
                pid = i
                # print(pid)
                at = random.randint(0, 15)
                complexity = random.randint(self.gpt_complex, self.gpt_complex + 3)
                bt = complexity * self.gpt_model
                self.createProcessFunction(pid, at, bt)
                i += 1
        else:
            i = self.scheduler.get_processes_length() + 1
            length = random.randint(3, 15) 
            for _ in range(length):
                pid = i
                at = random.randint(0, 15)
                bt = random.randint(1, 20)
                self.createProcessFunction(pid, at, bt)
                i += 1
        self.updateProcessNameFunction()

    def createProcessFunction(self, pid, at, bt):
        print(f"pid : {pid} : {type(pid)}, at = {at} : {type(at)}, bt = {bt} : {type(bt)}")
        row_count = self.tw_process.rowCount()
        self.tw_process.insertRow(row_count)
        self.tw_process.setItem(row_count, 0, QTableWidgetItem(f'P{pid:02}'))
        self.tw_process.setItem(row_count, 1, QTableWidgetItem(f'{at:02}'))
        self.tw_process.setItem(row_count, 2, QTableWidgetItem(f'{bt:02}'))

        # 가장 밑으로 자동 스크롤
        self.tw_process.scrollToBottom()

        # 프로세스의 색상 설정
        color = QColor(random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        
        # 프로세스 추가
        self.scheduler.add_process(pid, at, bt, color)

        # 배경색 설정
        item = self.tw_process.item(row_count, 0)
        item.setBackground(color)

    # del키로 프로세스 삭제
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.processRemoveFunction()
        else:
            super().keyPressEvent(event)

    # 프로세스 삭제
    def processRemoveFunction(self):
        selected_rows = sorted(
            set(index.row() for index in self.tw_process.selectedIndexes()), reverse=True)
        for row in selected_rows:
            process_id_item = self.tw_process.item(
                row, 0)  # process_id가 있는 열의 아이템 가져오기
            if process_id_item is not None:
                process_id = int(process_id_item.text()[1:3])
                self.scheduler.remove_process(process_id)
            self.tw_process.removeRow(row)
            self.updateProcessNameFunction()

        if len(selected_rows) == 0:
            QMessageBox.warning(self, '삭제 실패', f'선택된 행이 없습니다.')
        self.pb_remove.setVisible(False)

    # 열 선택시에만 삭제 버튼 가시화
    def rbVisibilityFunction(self):
        selected_row = self.tw_process.currentRow()
        if selected_row >= 0:
            self.pb_remove.setVisible(True)
        else:
            self.pb_remove.setVisible(False)

    # 알고리즘, 코어 선택
    def comboBoxFunction(self, flag, index):
        if flag == 1:  # p알고리즘 ComboBox
            if self.gb_Timeq.isVisible():
                self.gb_Timeq.setVisible(False)
            if self.gb_model.isEnabled():  # 처음에는 gb_model 비활성화
                self.gb_model.setEnabled(False)
                self.gb_model.setStyleSheet("color: lightgray")
            if self.gb_complex.isEnabled():  # 처음에는 gb_complex 비활성화
                self.gb_complex.setEnabled(False)
                self.gb_complex.setStyleSheet("color: lightgray")
            if not self.gb_add.isEnabled(): # gb_add 비활성화 시 다시 활성화
                self.gb_add.setEnabled(True)

            self.cb_algorithm.move(100, 60)
            if index != 0:
                text = self.cb_algorithm.currentText()
                QMessageBox.about(
                    self, '알고리즘 선택', f'{text} 알고리즘을 선택하셨습니다.')
                if index == 2:  # RR
                    self.gb_Timeq.setVisible(True)
                    self.cb_algorithm.move(10, 60)
                if index == 6:  # TRR
                    self.gb_model.setEnabled(True)
                    self.gb_complex.setEnabled(True)
                    self.gb_add.setEnabled(False) # 랜덤으로 프로세스를 추가시키기 위해 비활성화
                    self.gb_model.setStyleSheet("color: black")
                    self.gb_complex.setStyleSheet("color: black")
        else:  # Core 선택 ComboBox
            if index == 0:  # Off
                self.core[flag - 2] = 0
            elif index == 1:  # P-Core
                self.core[flag - 2] = 1
            else:  # E-Core
                self.core[flag - 2] = 2
            self.lb_core.setText(
                f"현재 코어: P-Core : {self.core.count(1)}개, E-Core : {self.core.count(2)}개")

    # GPT 모델 선택
    def GPTSelectFunction(self, flag):
        pushbutton = self.sender()  # 이벤트를 발생시킨 버튼 객체 가져오기
        
        if pushbutton.isChecked():  # 버튼을 누를 때
            if len(self.gpt_selected) == 0:
                self.gpt_selected.append((pushbutton, flag))
            else:
                # model 혹은 complex를 중복 선택했을 때의 예외처리
                if (self.gpt_selected[0][1] <= 2 and flag <= 2) or (self.gpt_selected[0][1] > 2 and flag > 2):
                    self.gpt_selected.clear()
                self.gpt_selected.append((pushbutton, flag))

            print(pushbutton.objectName(), self.gpt_selected)
            if flag <= 2:
                subject = getattr(self, 'pb_model2') if flag == 1 else getattr(
                    self, 'pb_model1')
                subject.setIcon(QIcon('logo/g_gpt-icon.png'))
                subject.setChecked(False)
                if flag == 1:
                    pushbutton.setIcon(QIcon('logo/gpt-icon.png'))
                else:
                    pushbutton.setIcon(QIcon('logo/gpt4-icon.png'))
            else:
                buttons = [getattr(self, 'pb_high'), getattr(self, 'pb_mid'), getattr(self, 'pb_low')]
                for i, button in enumerate(buttons):
                    if i + 3 == flag:
                        button.setIcon(QIcon('logo/complex.png'))
                        button.setChecked(True)
                    else:
                        button.setIcon(QIcon('logo/g_complex.png'))
                        button.setChecked(False)

        else:  # 버튼을 해제할 때
            if flag <= 2:
                pushbutton.setIcon(QIcon('logo/g_gpt-icon.png'))
                if self.gpt_model != -1:
                    self.gpt_model == -1
            else:
                pushbutton.setIcon(QIcon('logo/g_complex.png'))
                if self.gpt_complex != -1:
                    self.gpt_complex == -1
            # 객체 이름 비교, gpt_selected 리스트 내부의 tuple 삭제 (object, flag)
            for tup in self.gpt_selected:
                if tup[0].objectName() == pushbutton.objectName():
                    self.gpt_selected.remove(tup)
            print(self.gpt_selected)

        # model과 complex를 모두 선정 완료했을 때
        if len(self.gpt_selected) == 2:
            name = [0] * 2
            for tup in self.gpt_selected:
                flag = tup[1]
                if flag <= 2:
                    self.gpt_model = flag
                    name[0] = 3.0 + float(flag / 2)
                else:
                    if flag == 3: # high
                        self.gpt_complex = 9
                        name[1] = "High"
                    elif flag == 4: # mid
                        self.gpt_complex = 5
                        name[1] = "Mid"
                    else: # low
                        self.gpt_complex = 1
                        name[1] = "Low"
            reply = QMessageBox.question(self, '프로세스 생성', f'선택한 GPT 모델({name[0]})과 복잡도({name[1]})를 이용해서 프로세스들을 생성하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            

            if reply == QMessageBox.Yes:
                self.RandomAddProcessFunction(True)
            for tup in self.gpt_selected:
                if tup[1] <= 2:
                    tup[0].setIcon(QIcon('logo/g_gpt-icon.png'))
                else:
                    tup[0].setIcon(QIcon('logo/g_complex.png'))
                tup[0].setChecked(False)
                print(tup[0].objectName(),"이 해제되었습니다.")
                self.gpt_model = self.gpt_complex = -1
            self.gpt_selected.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    myWindow = OS_Scheduler()

    myWindow.show()

    app.exec_()

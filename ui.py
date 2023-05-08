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
        self.addProcessName = 0
        self.addArrivalTime = 0
        self.addBurstTime = 0

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

        self.gb_Timeq.setVisible(False)
        self.pb_remove.setVisible(False)

        # 프로세스 column 너비 변경 불가능
        self.tw_process.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

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

        # 메뉴 기능 연결
        self.a_exit.triggered.connect(QApplication.exit)

    # 프로세스 추가
    def processAddFunction(self, flag):
        if flag == 1:  # Name up
            self.addProcessName += 1
            self.lb_add_process.setText(f"P{self.addProcessName:02}")
        elif flag == 2:  # Name down
            if self.addProcessName > 0:
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
            self.addProcessName = 0
            self.addArrivalTime = 0
            self.addBurstTime = 0
            self.lb_add_process.setText(f"P{self.addProcessName:02}")
            self.lb_add_process_at.setText(f"{self.addArrivalTime:02}")
            self.lb_add_process_bt.setText(f"{self.addBurstTime:02}")
        elif flag == 8:  # save
            pid = f"P{self.addProcessName:02}"
            at = f"{self.addArrivalTime}"
            bt = f"{self.addBurstTime}"

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
                row_count = self.tw_process.rowCount()
                self.tw_process.insertRow(row_count)
                self.tw_process.setItem(row_count, 0, QTableWidgetItem(pid))
                self.tw_process.setItem(row_count, 1, QTableWidgetItem(at))
                self.tw_process.setItem(row_count, 2, QTableWidgetItem(bt))

                # 프로세스의 색상 설정
                color = QColor(random.randint(0, 255), random.randint(
                    0, 255), random.randint(0, 255))
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
                process_id = process_id_item.text()
                self.scheduler.remove_process(process_id)
            self.tw_process.removeRow(row)
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
                    self.gb_model.setStyleSheet("color: black")
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
            subject = getattr(self, 'pb_model2') if flag == 1 else getattr(
                self, 'pb_model1')
            subject.setIcon(QIcon('logo/g_gpt-icon.png'))
            subject.setChecked(False)
            pushbutton.setIcon(QIcon('logo/gpt-icon.png'))
        else:  # 버튼을 해제할 때
            pushbutton.setIcon(QIcon('logo/g_gpt-icon.png'))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    myWindow = OS_Scheduler()

    myWindow.show()

    app.exec_()

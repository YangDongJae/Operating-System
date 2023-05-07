import sys
import numpy as np
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class RRScheduler(QtWidgets.QMainWindow):
    def __init__(self):
        super(RRScheduler, self).__init__()

        # Set up the window
        self.setWindowTitle('Round Robin Scheduler')
        self.setGeometry(100, 100, 800, 600)

        # Create the Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)

        # Define the tasks and processors
        self.tasks = [
            {'name': 'Task 1', 'burst_time': 8},
            {'name': 'Task 2', 'burst_time': 4},
            {'name': 'Task 3', 'burst_time': 6}
        ]
        self.num_processors = 2

        # Set up the scheduler
        self.time_quantum = 3
        self.current_time = 0
        self.queue = []

        # Start the scheduling process
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.schedule)
        self.timer.start(1000)

    def schedule(self):
        # Clear the figure
        self.figure.clear()

        # Update the scheduler state
        if len(self.queue) == 0:
            self.current_time += 1
            for task in self.tasks:
                if task['burst_time'] > 0:
                    self.queue.append(task)
                    break
        else:
            current_task = self.queue.pop(0)
            if current_task['burst_time'] > self.time_quantum:
                current_task['burst_time'] -= self.time_quantum
                self.queue.append(current_task)
                self.current_time += self.time_quantum
            else:
                self.current_time += current_task['burst_time']
                current_task['burst_time'] = 0

        # Prepare the data for plotting
        labels = [task['name'] for task in self.tasks]
        burst_times = [task['burst_time'] for task in self.tasks]

        # Plot the Gantt chart
        ax = self.figure.add_subplot(111)
        ax.barh(0, burst_times[0], align='center', color='blue', label=labels[0])
        ax.barh(1, burst_times[1], align='center', color='orange', label=labels[1])
        ax.barh(2, burst_times[2], align='center', color='green', label=labels[2])
        ax.set_yticks([0, 1, 2])
        ax.set_yticklabels(labels)
        ax.set_xlabel('Time')
        ax.set_ylabel('Task')
        ax.set_title('Round Robin Scheduler (Time: {})'.format(self.current_time))
        ax.legend()

        # Draw the plot
        self.canvas.draw()

        # Check if all tasks are completed
        if all(task['burst_time'] == 0 for task in self.tasks):
            self.timer.stop()

if __name__ == '__main__':
    app= QtWidgets.QApplication(sys.argv)
    window = RRScheduler()
    window.show()
    sys.exit(app.exec_())

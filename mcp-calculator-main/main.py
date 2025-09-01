import threading
import mcp_pipe
import calculator

def run_mcp_pipe():
    # Call the main function or logic of your mcp_pipe.py script
    mcp_pipe.connect_with_retry():
() 

def run_calculator():
    # Call the main function or logic of your calculator.py script
    calculator.main_function()

if __name__ == "__main__":
    # Create threads for each script
    thread1 = threading.Thread(target=run_mcp_pipe)
    thread2 = threading.Thread(target=run_calculator)

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to complete (optional, depends on your scripts' behavior)
    thread1.join()
    thread2.join()
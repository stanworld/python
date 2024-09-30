package api

import (
	"fmt"
	"net/http"
	"sync"
	"time"
)

// TaskResult holds the result of the task
type TaskResult struct {
	ID     string
	Result string
}

var (
	taskStore = make(map[string]string)
	mu        sync.Mutex
)

// LongRunningTask simulates a long-running task
func LongRunningTask(id string, resultChan chan<- TaskResult) {
	// Simulate a long-running task
	time.Sleep(10 * time.Second)
	result := fmt.Sprintf("Result of task %s", id)

	// Send the result to the channel
	resultChan <- TaskResult{ID: id, Result: result}
}

// StartTaskHandler starts a new task and returns a task ID
func StartTaskHandler(w http.ResponseWriter, r *http.Request) {
	id := fmt.Sprintf("%d", time.Now().UnixNano())
	resultChan := make(chan TaskResult)

	go LongRunningTask(id, resultChan)

	go func() {
		result := <-resultChan
		mu.Lock()
		taskStore[result.ID] = result.Result
		mu.Unlock()
	}()

	fmt.Fprintf(w, "Task started with ID: %s\n", id)
}

// GetTaskResultHandler returns the result of a task if it's completed
func GetTaskResultHandler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	mu.Lock()
	result, exists := taskStore[id]
	mu.Unlock()

	if !exists {
		http.Error(w, "Task not found or still running", http.StatusNotFound)
		return
	}

	fmt.Fprintf(w, "Task %s result: %s\n", id, result)
}

//func main() {
//	http.HandleFunc("/start", StartTaskHandler)
//	http.HandleFunc("/result", GetTaskResultHandler)

//	fmt.Println("Server started at :8080")
//	log.Fatal(http.ListenAndServe(":8080", nil))
//}

// server: go run improve.go
// client: curl http://localhost:8080/start, polling result: http://localhost:8080/result?id=<task_id>

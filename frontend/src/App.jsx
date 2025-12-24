import Layout from './components/Layout'

function App() {
  return (
    <Layout>
      <div className="text-center">
        <h2 className="text-3xl font-semibold text-gray-900 mb-4">
          Welcome to Coffee Chat Scheduler
        </h2>
        <p className="text-gray-600">
          Book a time slot to schedule a coffee chat.
        </p>
      </div>
    </Layout>
  )
}

export default App

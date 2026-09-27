import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

const CATEGORIES = ['Carnivore', 'Omnivore', 'Herbivore']

const DINOSAURS = [
  {name: "Allosaurus", category: "Carnivore"},
  {name: "Austroraptor", category: "Carnivore"},
  {name: "Carnotaurus", category: "Carnivore"},
    {name: "Beipiaosaurus", category: "Omnivore"},
    {name: "Gallimimus", category: "Omnivore"},
    {name: "Diabloceratops", category: "Herbivore"},
    {name: "Dryosaurus", category: "Herbivore"}

]


function App() {
  const [category, setCategory] = useState(null)

  const list = category ? DINOSAURS.filter((d) => d.category == category) : []

  return (<main>
            <h1>The Isle</h1>
            <section>
              {CATEGORIES.map((c) => (
                  <button key={c}
                          onClick={() => setCategory(c)}
                          style={{ fontWeight: category === c ? "bold" : "normal"}}
                  >
                    {c}
                  </button>
              ))}
            </section>

            { category ? (
                <ul>
                  {list.map((d) => (
                      <li key={d.name}>{d.name}</li>
                  ))}
                </ul>): (
                    <p>Pick a category</p>
                )}
          </main>


  )
}

export default App

import React from 'react'
import Game from './Game'

const isActive = (roundStart, roundEnd) => {
    const now = new Date()
    const start = new Date(Date.parse(roundStart))
    const end = new Date(Date.parse(roundEnd))

    return start < now && end > now
}

const sortByDate = (a, b) => new Date(a.start_date) - new Date(b.start_date)

const Round = ({ round }) => {
    const active = isActive(round.start_date, round.stop_date)

    // sort game by date
    round.games.sort(sortByDate)

    return (
        <div className={active ? 'round active' : 'round inactive'}>
            <h2>{round.name}</h2>
            <div className='round-headers'>
                <h6 className='deadline'>Deadline</h6>
                <h6 className='matchup'>Match (grupp)</h6>
                <h6 className='res'>Resultat</h6>
                <h6 className='bet'>Tips</h6>
                <h6 className='pts'>Poäng</h6>
            </div>
            {round.games.map((g, i) => <Game key={i} game={g} />)} 
        </div>
    )
}

export default Round

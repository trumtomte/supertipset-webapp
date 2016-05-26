import fetch from 'isomorphic-fetch'
import { successNotification } from './notification'
import { assign, preparePut, preparePost } from './utils'

const INVALIDATE = 'supertipset/user/INVALIDATE'
// User
const REQUEST = 'supertipset/user/REQUEST'
const RECEIVE = 'supertipset/user/RECEIVE'
// Place bet 
const REQUEST_BET = 'supertipset/user/REQUEST_BET'
const RECEIVE_BET = 'supertipset/user/RECEIVE_BET'
// Place special bet
const REQUEST_SPECIAL_BET = 'supertipset/user/REQUEST_SPECIAL_BET'
const RECEIVE_SPECIAL_BET = 'supertipset/user/RECEIVE_SPECIAL_BET'
// Change user password
const REQUEST_EDIT_PASSWORD = 'supertipset/user/REQUEST_EDIT_PASSWORD'
const RECEIVE_EDIT_PASSWORD = 'supertipset/user/RECEIVE_EDIT_PASSWORD'

const initialState = {
    isFetching: false,
    didInvalidate: false,
    id: window.userID,
    data: {}
}

export default function reducer(state = initialState, action) {
    switch (action.type) {
        case INVALIDATE:
            return assign(state, {
                didInvalidate: true
            })
        case REQUEST:
            return assign(state, {
                isFetching: true,
                didInvalidate: false
            })
        case RECEIVE:
            return assign(state, {
                isFetching: false,
                didInvalidate: false,
                data: action.user
            })
        case RECEIVE_BET:
            return assign(state, {
                data: assign(state.data, {
                    bets: state.data.bets.concat(action.bet)
                })
            })
        case RECEIVE_SPECIAL_BET:
            return assign(state, {
                data: assign(state.data, {
                    special_bets: state.data.special_bets.concat(action.specialBet)
                })
            })
        // TODO listen to all actions?
        default:
            return state
    }
}

export function invalidateUser() {
    return { type: INVALIDATE }
}

export function requestUser() {
    return { type: REQUEST }
}

export function receiveUser(user) {
    return { type: RECEIVE, user }
}

function shouldFetch(user) {
    if (user.isFetching) {
        return false
    } else if (!user.data.hasOwnProperty('id')) {
        return true 
    } else {
        return user.didInvalidate
    }
}

export function fetchUser(id, tournament) {
    return (dispatch, getState) => {
        const { user } = getState()

        if (!shouldFetch(user)) {
            return Promise.resolve()
        }

        dispatch(requestUser())

        const url = `http://localhost:8001/api/users/${id}/detail/?tournament=${tournament}`

        return fetch(url)
            .then(res => {
                if (res.ok) {
                    res.json().then(json => dispatch(receiveUser(json)))
                } else {
                    // TODO error handling
                    console.log('unable to fetch user')
                }
            })
    }
}

export function requestEditUserPassword() {
    return { type: REQUEST_EDIT_PASSWORD }
}

export function receiveEditUserPassword(user) {
    return { type: RECEIVE_EDIT_PASSWORD, user }
}

export function editUserPassword(id, username, password) {
    return dispatch => {
        dispatch(requestEditUserPassword())

        const payload = preparePut({
            id,
            username,
            password
        })

        const url = `http://127.0.0.1:8001/api/users/${id}/password/`

        return fetch(url, payload)
            .then(res => {
                if (res.ok) {
                    res.json().then(json => {
                        dispatch(receiveEditUserPassword(json))
                        // TODO better notification message?
                        dispatch(successNotification('Du har redigerat ditt lösenord!'))
                    })
                } else {
                    // TODO Error handling
                    console.log('unable to change user password')
                }
            })
    }
}

export function requestBet() {
    return { type: REQUEST_BET }
}

export function receiveBet(bet) {
    return { type: RECEIVE_BET, bet }
}

export function placeBet(user, game, betTeamOne, betTeamTwo) {
    return dispatch => {
        dispatch(requestBet())

        const payload = preparePost({
            user,
            game,
            team_1_bet: betTeamOne,
            team_2_bet: betTeamTwo
        })

        const url = 'http://localhost:8001/api/bets/'

        return fetch(url, payload)
            .then(res => {
                if (res.ok) {
                    res.json().then(json => {
                        dispatch(receiveBet(json))
                        // TODO better notification message?
                        dispatch(successNotification('Tips sparat!'))
                    })
                } else {
                    // TODO error handling
                    console.log('unable to place bet')
                }
            })
    }
}

export function requestSpecialBet() {
    return { type: REQUEST_SPECIAL_BET }
}

export function receiveSpecialBet(specialBet) {
    return { type: RECEIVE_SPECIAL_BET, specialBet }
}

export function placeSpecialBet(user, player, goals, team, tournament) {
    return dispatch => {
        dispatch(requestSpecialBet())

        const payload = preparePost({
            user,
            team,
            player,
            tournament,
            player_goals: goals
        })

        const url = 'http://localhost:8001/api/specialbets/'

        return fetch(url, payload)
            .then(res => {
                if (res.ok) {
                    res.json().then(json => {
                        dispatch(receiveSpecialBet(json))
                        // TODO better notification message?
                        dispatch(successNotification('Specialtips sparat!'))
                    })
                } else {
                    // TODO error handling
                    console.log('unable to place special bet')
                }
            })
    }
}

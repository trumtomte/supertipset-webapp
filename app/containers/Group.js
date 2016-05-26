import React, { Component } from 'react'
import { connect } from 'react-redux'
import { fetchGroup } from '../ducks/group'
import { GroupMembers, BackButton } from '../components'
import EditGroupDescriptionButton from './EditGroupDescriptionButton'
import EditGroupPasswordButton from './EditGroupPasswordButton'

class Group extends Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        const { dispatch, params, tournament } = this.props

        if (params.hasOwnProperty('id')) {
            dispatch(fetchGroup(params.id, tournament))
        }
    }

    render() {
        const { params, group, user, dispatch } = this.props

        // TODO wont need this?
        if (!params.hasOwnProperty('id')) {
            return <p>Gruppen finns inte</p>
        }

        if (group.isFetching || group.data.length === 0) {
            return <p>Ingen grupp</p>
        }

        const isAdmin = user.id === group.data.admin.id

        return (
            <GroupMembers group={group.data}>
                <BackButton />
                {isAdmin ? <EditGroupPasswordButton group={group.data} /> : ''}
                <h2 className='group-title'>
                    {group.data.name} {isAdmin ? <small>(admin)</small> : ''}
                </h2>
                <p className='group-description'>
                    {group.data.description}
                    {isAdmin ? <EditGroupDescriptionButton group={group.data} /> : ''}
                </p>
            </GroupMembers>
        )
        
    }
}

export default connect(
    // State to props
    state => ({
        user: state.user,
        group: state.group,
        tournament: state.tournament
    })
)(Group)

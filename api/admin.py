import string
import random
from collections import defaultdict
from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import User, Group, Tournament, Round, Team, Game, Player, Bet, \
        SpecialBet, SpecialBetResult, Point, Result, Goal, SpecialBetFinal

class GroupAdmin(admin.ModelAdmin):
    """
    Group
    """
    list_display = ('name', 'admin', 'created_at')
    search_fields = ('name', 'admin__username')

class RoundAdmin(admin.ModelAdmin):
    """
    Round
    """
    list_display = ('name', 'tournament', 'start_date', 'stop_date')
    search_fields = ('name', 'tournament__name')

class TeamAdmin(admin.ModelAdmin):
    """
    Team
    """
    list_display = ('name', 'country', 'created_at')
    search_fields = ('name', 'country')

class GameAdmin(admin.ModelAdmin):
    """
    Game
    """
    list_display = ('team_1', 'team_2', 'group_name', 'round',
                    'start_date')
    search_fields = ('team_1__name', 'team_2__name', 'group_name',
                     'round__name')

class PlayerAdmin(admin.ModelAdmin):
    """
    Player
    """
    list_display = ('firstname', 'lastname', 'created_at')
    search_fields = ('firstname', 'lastname')

class BetAdmin(admin.ModelAdmin):
    """
    Bet
    """
    list_display = ('username', 'fullname', 'game', 'team_1_bet',
                    'team_2_bet', 'created_at')

    search_fields = ('user__username', 'user__firstname', 'user__lastname')

    def username(self, obj):
        return obj.user.username

    def fullname(self, obj):
        return '{} {}'.format(obj.user.firstname, obj.user.lastname)

    username.short_description = 'Username'
    fullname.short_description = 'Fullname'

class SpecialBetAdmin(admin.ModelAdmin):
    """
    Special bet
    """
    list_display = ('user', 'team', 'player', 'player_goals',
                    'tournament')
    search_fields = ('user__username', 'team__name')

class SpecialBetResultAdmin(admin.ModelAdmin):
    """
    Special bet result
    """
    list_display = ('user', 'team', 'player', 'goals', 'tournament')
    search_fields = ('user__username', 'user__firstname', 'user__lastname')

class SpecialBetFinalAdmin(admin.ModelAdmin):
    """
    Special bet final
    """
    list_display = ('tournament', 'team', 'created_at')

class PointAdmin(admin.ModelAdmin):
    """
    Point
    """
    list_display = ('username', 'fullname', 'points', 'result')
    search_fields = ('user__username', 'user__firstname', 'user__lastname')

    def username(self, obj):
        return obj.user.username

    def fullname(self, obj):
        return '{} {}'.format(obj.user.firstname, obj.user.lastname)

    username.short_description = 'Username'
    fullname.short_description = 'Fullname'

class GoalAdmin(admin.ModelAdmin):
    """
    Goal
    """
    list_display = ('player', 'game', 'goals')
    search_fields = ('player__firstname', 'player__lastname',
                     'game__team_1__name', 'game__team_2__name')

class UserAdmin(admin.ModelAdmin):
    """
    User
    """
    list_display = ('username', 'email', 'firstname', 'lastname', 'created_at')
    search_fields = ('user__username', 'user__firstname', 'user__lastname')
    actions = ['reset_password_action']

    def reset_password_action(self, request, queryset):
        # Only extract first user
        user = queryset[0]

        try:
            new_temp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            user.password = make_password(new_temp_pass)
            user.save()
        except Exception:
            print("Unable to make a new temp password for a user")
            self.message_user(request, "Unable to make a new temp password for a user")
            return False

        self.message_user(request, 'New password generated! -> {}'.format(new_temp_pass))


    reset_password_action.short_description = 'Reset password for a user'

def calculate_points(t1, t2, b1, b2):
    """
    Takes number of goals for each team (team 1 & team 2) and compares them
    with user bets (bet 1 & bet 2) and then calculates the points.
    """
    # Perfect bet
    if t1 == b1 and t2 == b2:
        return 10

    # Start points at 0
    points = 0
    # Calculate goal/bet difference
    tDiff = t1 - t2
    bDiff = b1 - b2

    # One bet is the same amount of goals for one team
    if t1 == b1 or t2 == b2:
        points += 1

    # Team 1 won
    if tDiff > 0 and bDiff > 0:
        points += 4
    # Team 2 won
    elif tDiff < 0 and bDiff < 0:
        points += 4
    # Draw
    elif tDiff == 0 and bDiff == 0:
        points += 4

    return points

class ResultAdmin(admin.ModelAdmin):
    list_display = ('game', 'team_1_goals', 'team_2_goals')
    search_fields = ('game__team_1__name', 'game__team_2__name')
    actions = ['calculate_points_action']

    def calculate_points_action(self, request, queryset):
        bulk_points = []

        # All results from games 
        for result in queryset:
            t1 = result.team_1_goals
            t2 = result.team_2_goals
            game = result.game

            # All bets placed on the game by users
            bets = Bet.objects.filter(game=game.id)

            for bet in bets:
                b1 = bet.team_1_bet
                b2 = bet.team_2_bet
                user = bet.user
                points = calculate_points(t1, t2, b1, b2)
                p = Point(user=user, points=points, result=result)
                bulk_points.append(p)

                # NOTE: old way
                try:
                    p = Point(user=user, points=points, result=result)
                    p.save()
                except Exception:
                    print("<Point> object already exists for user.")

        # try:
        #     Point.objects.bulk_create(bulk_points)
        # except Exception:
        #     print("Unable to perform a bulk_create on <Point>")
        #     self.message_user(request, 'Unable to calculate points')
        #     return False

        self.message_user(request, 'Points has been calculated!')

    # Dropdown menu text
    calculate_points_action.short_description = 'Calculate points'

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'stop_date')
    actions = ['calculate_points_action']

    def calculate_points_action(self, request, queryset):
        bulk_points = []

        for tournament in queryset:
            # special bets from users
            special_bets = SpecialBet.objects.filter(tournament=tournament.id)
            correct_bets = SpecialBetFinal.objects.prefetch_related('players') \
                                          .filter(tournament=tournament.id)

            if len(correct_bets) == 0:
                self.message_user(request, 'There are no final special bet ' \
                                           'results available!')
                return False

            correct_bet = correct_bets[0]

            for special_bet in special_bets:
                player_points = 0
                goals_points = 0
                team_points = 0

                # Correct player
                if special_bet.player in correct_bet.players.all():
                    player_points = 20

                    # Correct number of goals
                    if special_bet.player_goals == correct_bet.goals:
                        goals_points = 20

                # Correct team
                if special_bet.team.id == correct_bet.team.id:
                    team_points = 30

                result = SpecialBetResult(user=special_bet.user,
                                          tournament=tournament,
                                          player=player_points,
                                          goals=goals_points,
                                          team=team_points)
                bulk_points.append(result)

                # NOTE: old way
                try:
                    result = SpecialBetResult(user=special_bet.user,
                                              tournament=tournament,
                                              player=player_points,
                                              goals=goals_points,
                                              team=team_points)
                    result.save()
                except Exception:
                    print("<SpecialBetResult> object already exists for user.")

        # try:
        #     SpecialBetResult.objects.bulk_create(bulk_points)
        # except Exception:
        #     print("Unable to perform bulk_create on <SpecialBetResult>")
        #     self.message_user(request, 'Unable to calculate points')
        #     return False
        
        self.message_user(request, 'Points has been calculated!')

    # Dropdown menu text
    calculate_points_action.short_description = 'Calculate points'


# Register models and admin models
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(SpecialBet, SpecialBetAdmin)
admin.site.register(SpecialBetResult, SpecialBetResultAdmin)
admin.site.register(SpecialBetFinal)
admin.site.register(Point, PointAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Result, ResultAdmin)

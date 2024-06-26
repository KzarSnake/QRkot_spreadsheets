from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import FORMAT


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет на {now_date_time}',
            'locale': 'ru_RU',
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': 'Лист1',
                    'gridProperties': {'rowCount': 100, 'columnCount': 11},
                }
            }
        ],
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
    spreadsheetid: str, wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list,
    wrapper_services: Aiogoogle,
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Проекты по скорости закрытия'],
        ['Проект', 'Срок сбора', 'Описание'],
        *[list(map(str, project.values())) for project in projects],
    ]
    update_body = {'majorDimension': 'ROWS', 'values': table_values}
    all_lines = len(table_values)
    if all_lines >= 100:
        raise Exception('Превышен лимит строк')

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{all_lines}C{all_lines}',
            valueInputOption='USER_ENTERED',
            json=update_body,
        )
    )
